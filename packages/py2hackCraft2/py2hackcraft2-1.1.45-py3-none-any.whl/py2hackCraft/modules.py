import websocket
import threading
import time
import json
import logging
from dataclasses import dataclass
from typing import Callable, Any, List, Optional, NamedTuple

def str_to_bool(s):
    """
    文字列をブール値に変換する

    Args:
        s (str): "true" または "false"（大文字小文字は無視）

    Returns:
        bool: 変換されたブール値"true"ならTrue、"false"ならFalse
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot covert {s} to a boolean.")  # 有効な文字列でない場合はエラー

class UninitializedClientError(Exception):
    """
    WebSocketClientが初期化されていないことを示すカスタム例外

    :category: 基本クラス
    """
    pass


class _WebSocketClient:
    """
    WebSocketクライアントを表すクラス

    :category: 基本クラス
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.connected = False
        self.response_event = threading.Event()
        self.callbacks = {}

    def connect(self, host: str, port: int):
        self.host = host
        self.port = port
        self.url = "ws://%s:%d/ws" % (host, port)
        logging.debug("connecting '%s'" % (self.url))
        self.connected = False
        self.ws = websocket.WebSocketApp(self.url,
                                       on_message=self._on_message,
                                       on_error=self._on_error,
                                       on_close=self._on_close)
        self.ws.on_open = self._on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self._run_forever()

    def disconnect(self):
        self.connected = False
        self.host = None
        self.port = None
        self.close()

    def set_callback(self, event_name, callback_func):
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback_func)

    def _on_message(self, ws, message):
        logging.debug("on_message '%s'" % message)
        try:
            json_message = json.loads(message)
            type = json_message['type']
            data = json_message['data']
            if type == 'result':
                self.result = data
            elif type == 'error':
                self.error = data
            elif type == 'logged':
                self.connected = True
                self.result = data
            elif type == 'attach':
                self.result = data
            elif type == 'event':
                json_event = json.loads(data)
                event_name = json_event['name']
                logging.debug("on event %s '%s'" % (event_name, json_event['data']))
                if event_name in self.callbacks:
                    for callback in self.callbacks[event_name]:
                        callback_thread = threading.Thread(target=callback, args=(json_event['data'],))
                        callback_thread.start()
                        return
                if json_event['data']:
                    self.result = json_event['data']
                    self.response_event.set()
                return
            else:
                self.result = data
            self.response_event.set()
        except json.JSONDecodeError:
            logging.error("JSONDecodeError '%s'" % message)

    def _on_error(self, ws, error):
        logging.debug("on_error '%s'" % error)

    def _on_close(self, ws, close_status_code, close_msg):
        logging.debug("### closed ###")
        self.connected = False

    def _on_open(self, ws):
        logging.debug("Opened connection")
        self.connected = True

    def _run_forever(self):
        self.thread.start()

    def _wait_for_connection(self):
        while not self.connected:
            time.sleep(0.1)


    def send(self, message):
        logging.debug("send sending'%s'" % message)
        self._wait_for_connection()
        with self.lock:
            self.result = None
            self.response_event.clear()
            self.ws.send(message)
            self.response_event.wait()
        return self.result

    def close(self):
        self.ws.close()
        self.thread.join()

    def wait_for(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args
        message = {
            "type": "hook",
            "data": data
        }
        self.send(json.dumps(message))

    def send_call(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args
        message = {
            "type": "call",
            "data": data
        }
        self.send(json.dumps(message))

class Coord(NamedTuple):
    """
    座標を表す名前付きタプル

    :category: データクラス

    Attributes:
        x (int): X座標
        y (int): Y座標
        z (int): Z座標
        cord (str): 座標系 ("": 絶対座標, "~": 相対座標, "^": ローカル座標)
    """
    x: int
    y: int
    z: int
    cord: str

@dataclass(frozen=True)
class Location:
    """
    座標を表すデータクラス

    :category: データクラス

    Attributes:
        x (int): X座標
        y (int): Y座標
        z (int): Z座標
        world (str): ワールド名（デフォルトは"world"）
        cord (str): 座標系（デフォルトは""（絶対座標））

            - "": 絶対座標 (例: 100, 64, -200)

            - "~": 相対座標 (例: ~10, ~0, ~-5)

            - "^": ローカル座標 (例: ^0, ^5, ^0)
    """
    x: int
    y: int
    z: int
    world: str = "world"
    cord: str = ""  # デフォルトは絶対座標

class LocationFactory:
    """
    Minecraftの座標を生成するファクトリクラス

    :category: データクラス
    
    座標系の種類:

    - ABSOLUTE: 絶対座標 (例: 100, 64, -200)

    - RELATIVE: 相対座標 (例: ~10, ~0, ~-5)

    - LOCAL: ローカル座標 (例: ^0, ^5, ^0)
    """
    ABSOLUTE = ""  # 絶対座標 (例: 100, 64, -200)
    RELATIVE = "~"  # 相対座標 (例: ~10, ~0, ~-5)
    LOCAL = "^"     # ローカル座標 (例: ^0, ^5, ^0)

    @staticmethod
    def absolute(x: int, y: int, z: int, world: str = "world") -> Location:
        """
        絶対座標を生成する
        
        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            world (str, optional): ワールド名. デフォルトは"world".
            
        Returns:
            Location: 生成された絶対座標
            
        Example:
            .. code-block:: python

                loc = LocationFactory.absolute(100, 64, -200)
                print(f"X: {loc.x}, Y: {loc.y}, Z: {loc.z}, ワールド: {loc.world}, 座標系: {loc.cord}")
        """
        return Location(x, y, z, world, LocationFactory.ABSOLUTE)
    
    @staticmethod
    def relative(x: int, y: int, z: int, world: str = "world") -> Location:
        """
        相対座標を生成する（自分を中心とした東西南北）
        
        Args:
            x (int): 東(+)西(-)方向の相対距離
            y (int): 上(+)下(-)方向の相対距離
            z (int): 南(+)北(-)方向の相対距離
            world (str, optional): ワールド名. デフォルトは"world".
            
        Returns:
            Location: 生成された相対座標
            
        Example:
            .. code-block:: python

                loc = LocationFactory.relative(10, 0, -5)  # 東に10、北に5進む
                print(f"X: {loc.x}, Y: {loc.y}, Z: {loc.z}, ワールド: {loc.world}, 座標系: {loc.cord}")
        """
        return Location(x, y, z, world, LocationFactory.RELATIVE)
    
    @staticmethod
    def local(x: int, y: int, z: int, world: str = "world") -> Location:
        """
        ローカル座標を生成する（自分の向きを基準とした前後左右）
        
        Args:
            x (int): 右(+)左(-)方向の相対距離
            y (int): 上(+)下(-)方向の相対距離
            z (int): 前(+)後(-)方向の相対距離
            world (str, optional): ワールド名. デフォルトは"world".
            
        Returns:
            Location: 生成されたローカル座標
            
        Example:
            .. code-block:: python

                loc = LocationFactory.local(0, 5, 0)  # 自分の真上5ブロック
                print(f"X: {loc.x}, Y: {loc.y}, Z: {loc.z}, ワールド: {loc.world}, 座標系: {loc.cord}")
        """
        return Location(x, y, z, world, LocationFactory.LOCAL)

class Side:
    """
    ブロックの配置方向を表すデータクラス

    :category: データクラス
    """
    right = "Right"
    left = "Left"
    front = "Front"
    back = "Back"
    top = "Top"
    bottom = "Bottom"

@dataclass(frozen=True)
class InteractEvent:
    """
    クリックイベントを表すデータクラス

    :category: イベントクラス

    Attributes:
        action (str): アクションの名前
        player (str): クリックしたプレイヤー名
        player_uuid (str): クリックしたプレイヤーの一意の識別子（UUID）
        event (str): アイテムに設定されている名前
        name (str): ブロックあるいはエンティティーの名前
        type (str): ブロックあるいはエンティティーの種類
        data (int): ブロックのデータ値
        world (str): ブロックあるいはエンティティーのいたワールド名
        x (int): クリックした場所のワールドにおけるX座標
        y (int): クリックした場所のワールドにおけるY座標
        z (int): クリックした場所のワールドにおけるZ座標
    """
    action: str
    player: str
    player_uuid: str
    event: str
    name: str
    type: str
    data: int = 0
    world: str = "world"
    x: int = 0 
    y: int = 0 
    z: int = 0

@dataclass(frozen=True)
class EventMessage:
    """
    イベントメッセージを表すデータクラス

    :category: イベントクラス

    Attributes:
        entityUuid (str): イベントを送信したエンティティの一意の識別子（UUID）
        sender (str): 送信者の名前
        uuid (str): 送信者の一意の識別子（UUID）
        message (str): イベントメッセージの内容
    """
    entityUuid: str
    sender: str
    uuid: str
    message: str


@dataclass(frozen=True)
class ChatMessage:
    """
    チャットメッセージを表すデータクラス

    :category: イベントクラス

    Attributes:
        player (str): プレイヤー名
        uuid (str): プレイヤーの一意の識別子（UUID）
        entityUuid (str): チャットを送信したエンティティの一意の識別子（UUID）
        message (str): プレイヤーがチャットで送信したメッセージの内容
    """
    player: str
    uuid: str
    entityUuid: str
    message: str

@dataclass(frozen=True)
class RedstonePower:
    """
    レッドストーン信号を表すデータクラス

    :category: イベントクラス

    Attributes:
        entityUuid (str): レッドストーン信号を検出したエンティティの一意の識別子（UUID）
        oldCurrent (int): 前のレッドストーン信号の強さ
        newCurrent (int): 最新のレッドストーン信号の強さ
    """
    entityUuid: str
    oldCurrent: int
    newCurrent: int

@dataclass(frozen=True)
class Block:
    """
    ブロックを表すデータクラス

    :category: データクラス

    Attributes:
        name (str): ブロックの種類
        data (int): ブロックのデータ値
        isLiquid (bool): 液体ブロックかどうか
        isAir (bool): 空気ブロックかどうか
        isBurnable (bool): 燃えるブロックかどうか
        isFuel (bool): 燃料ブロックかどうか
        isOccluding (bool): 透過しないブロックかどうか
        isSolid (bool): 壁のあるブロックかどうか
        isPassable (bool): 通過可能なブロックかどうか
        world (str): ブロックが存在するワールドの名前（デフォルトは"world"）
        x (int): ブロックのX座標
        y (int): ブロックのY座標
        z (int): ブロックのZ座標
    """
    name: str
    type: str = "block"
    data: int = 0
    isLiquid: bool = False
    isAir: bool = False
    isBurnable: bool = False
    isFuel: bool = False
    isOccluding: bool = False
    isSolid: bool = False
    isPassable: bool = False
    x: int = 0
    y: int = 0
    z: int = 0
    world: str = "world"

@dataclass(frozen=True)
class ItemStack:
    """
    アイテムスタックを表すデータクラス

    :category: データクラス

    Attributes:
        slot (int): スロット番号
        name (str): アイテムの名前
        amount (int): アイテムの数量
    """
    slot: int = 0
    name: str = "air"
    amount: int = 0

class Player:
    """
    プレイヤーを表すクラス

    :category: 基本クラス
    """
    def __init__(self, player: str):
        self.name = player

    def login(self, host: str, port: int) -> 'Player':
        self.client = _WebSocketClient()
        self.client.connect(host, port)
        self.client.send(json.dumps({
            "type": "login",
            "data": {
                "player": self.name,
            }
        }))
        logging.debug("login '%s'" % self.client.result)
        self.uuid = self.client.result['playerUUID']
        self.world = self.client.result['world']
        return self

    def logout(self):
        self.client.disconnect()    

    def get_entity(self, name: str) -> 'Entity': 
        """
        指定された名前のエンティティを取得する

        Args:
            name (str): エンティティの名前

        Returns:
            Entity: 取得したエンティティ

        Raises:
            UninitializedClientError: クライアントが初期化されていない場合        
        """
        if self.client is None or not self.client.connected:  # 接続状態をチェック
            raise UninitializedClientError("Client is not initialized")

        message = {
            "type": "attach",
            "data": {"entity": name}
        }
        self.client.send(json.dumps(message))
        result = self.client.result
        if(result is None):
            raise ValueError("Entity '%s' not found" % name)
        
        entity = Entity(self.client, self.world, result)
        #ロールバックできるように設定
        self.client.send(json.dumps({
            "type": "start",
            "data": {"entity": entity.uuid}
        }))
        return entity

class Inventory:
    """
    インベントリを表すクラス

    :category: 基本クラス
    
    このクラスは、アルゴリズム学習のための基本的な操作を提供します。
    検索、ソート、集計などの操作は、このクラスの基本操作を組み合わせて実装できます。
    """
    def __init__(self, client: _WebSocketClient, entity_uuid: str, world: str, x: int, y: int, z: int, size: int, items: list):
        self.client = client
        self.entity_uuid = entity_uuid
        self.location = Location(x, y, z, world)
        self.size = size
        self.items = items

    def get_item(self, slot: int) -> ItemStack:
        """
        指定されたスロットのアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号

        Returns:
            ItemStack: 取得したアイテムの情報

        Example:
            .. code-block:: python

                # スロット0のアイテムを取得
                item = inventory.get_item(0)
                print(f"アイテム: {item.name}, 数量: {item.amount}")
        """
        self.client.send_call(self.entity_uuid, "getInventoryItem", [self.location.x, self.location.y, self.location.z, slot, self.location.cord])
        item_stack = ItemStack(** json.loads(self.client.result))
        return item_stack

    def get_all_items(self) -> List[ItemStack]:
        """
        インベントリ内の全てのアイテムを取得する

        Returns:
            List[ItemStack]: アイテムのリスト

        Example:
            .. code-block:: python

                # 全てのアイテムを取得して表示
                items = inventory.get_all_items()
                for item in items:
                    print(f"スロット{item.slot}: {item.name} x{item.amount}")
        """
        items = []
        for slot in range(self.size):
            item = self.get_item(slot)
            if item.name != "air":  # 空のスロットは除外
                items.append(item)
        return items

    def swap_items(self, slot1: int, slot2: int):
        """
        2つのスロットのアイテムを入れ替える

        Args:
            slot1 (int): 入れ替え元のスロット番号
            slot2 (int): 入れ替え先のスロット番号

        Example:
            .. code-block:: python

                # スロット0と1のアイテムを入れ替え
                inventory.swap_items(0, 1)
        """
        self.client.send_call(self.entity_uuid, "swapInventoryItem", [self.location.x, self.location.y, self.location.z, slot1, slot2, self.location.cord])

    def move_item(self, from_slot: int, to_slot: int):
        """
        アイテムを別のスロットに移動する

        Args:
            from_slot (int): 移動元のスロット番号
            to_slot (int): 移動先のスロット番号

        Example:
            .. code-block:: python

                # スロット0のアイテムをスロット5に移動
                inventory.move_item(0, 5)
        """
        self.client.send_call(self.entity_uuid, "moveInventoryItem", [self.location.x, self.location.y, self.location.z, from_slot, to_slot, self.location.cord])

    def retrieve_to_self(self, from_slot: int, to_slot: int):
        """
        チェストから自分のインベントリにアイテムを取り出す

        Args:
            from_slot (int): チェストの取り出し元スロット番号
            to_slot (int): 自分のインベントリの格納先スロット番号

        Example:
            .. code-block:: python

                # チェストのスロット0のアイテムを自分のスロット5に取り出す
                inventory.retrieve_from_self(0, 5)
        """
        self.client.send_call(self.entity_uuid, "retrieveInventoryItem", [self.location.x, self.location.y, self.location.z, to_slot, from_slot, self.location.cord])

    def store_from_self(self, from_slot: int, to_slot: int):
        """
        自分のインベントリからチェストにアイテムを格納する

        Args:
            from_slot (int): 自分のインベントリの取り出し元スロット番号
            to_slot (int): チェストの格納先スロット番号

        Example:
            .. code-block:: python

                # 自分のスロット0のアイテムをチェストのスロット5に格納
                inventory.store_to_self(0, 5)
        """
        self.client.send_call(self.entity_uuid, "storeInventoryItem", [self.location.x, self.location.y, self.location.z, from_slot, to_slot, self.location.cord])

class Volume:
    """
    3D空間の領域を表すクラス

    :category: データクラス
    
    座標系の種類:
    - ABSOLUTE: 絶対座標 (例: 100, 64, -200)
    - RELATIVE: 相対座標 (例: ~10, ~0, ~-5)
    - LOCAL: ローカル座標 (例: ^0, ^5, ^0)
    """
    ABSOLUTE = ""  # 絶対座標 (例: 100, 64, -200)
    RELATIVE = "~"  # 相対座標 (例: ~10, ~0, ~-5)
    LOCAL = "^"     # ローカル座標 (例: ^0, ^5, ^0)

    @staticmethod
    def absolute(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> 'Volume':
        """
        絶対座標で領域を指定する
        
        Args:
            x1 (int): 1つ目の座標のX座標
            y1 (int): 1つ目の座標のY座標
            z1 (int): 1つ目の座標のZ座標
            x2 (int): 2つ目の座標のX座標
            y2 (int): 2つ目の座標のY座標
            z2 (int): 2つ目の座標のZ座標
            
        Returns:
            Volume: 指定された領域
            
        Example:
            >>> # 絶対座標(100, 64, -200)から(110, 70, -190)の領域を定義
            >>> Volume.absolute(100, 64, -200, 110, 70, -190)
        """
        return Volume(x1, y1, z1, x2, y2, z2, Volume.ABSOLUTE)
    
    @staticmethod
    def relative(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> 'Volume':
        """
        相対座標で領域を指定する（自分を中心とした東西南北）
        
        Args:
            x1 (int): 1つ目の座標の東(+)西(-)方向の相対距離
            y1 (int): 1つ目の座標の上(+)下(-)方向の相対距離
            z1 (int): 1つ目の座標の南(+)北(-)方向の相対距離
            x2 (int): 2つ目の座標の東(+)西(-)方向の相対距離
            y2 (int): 2つ目の座標の上(+)下(-)方向の相対距離
            z2 (int): 2つ目の座標の南(+)北(-)方向の相対距離
            
        Returns:
            Volume: 指定された領域
            
        Example:
            >>> # 自分の周囲5ブロックの領域を定義
            >>> Volume.relative(-5, -5, -5, 5, 5, 5)
        """
        return Volume(x1, y1, z1, x2, y2, z2, Volume.RELATIVE)
    
    @staticmethod
    def local(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> 'Volume':
        """
        ローカル座標で領域を指定する（自分の向きを基準とした前後左右）
        
        Args:
            x1 (int): 1つ目の座標の右(+)左(-)方向の相対距離
            y1 (int): 1つ目の座標の上(+)下(-)方向の相対距離
            z1 (int): 1つ目の座標の前(+)後(-)方向の相対距離
            x2 (int): 2つ目の座標の右(+)左(-)方向の相対距離
            y2 (int): 2つ目の座標の上(+)下(-)方向の相対距離
            z2 (int): 2つ目の座標の前(+)後(-)方向の相対距離
            
        Returns:
            Volume: 指定された領域
            
        Example:
            >>> # 自分の周囲5ブロックの領域を定義（向きに依存）
            >>> Volume.local(-5, -5, -5, 5, 5, 5)
        """
        return Volume(x1, y1, z1, x2, y2, z2, Volume.LOCAL)

    def __init__(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, cord: str = ""):
        """
        領域を定義する
        
        Args:
            x1 (int): 1つ目の座標のX座標
            y1 (int): 1つ目の座標のY座標
            z1 (int): 1つ目の座標のZ座標
            x2 (int): 2つ目の座標のX座標
            y2 (int): 2つ目の座標のY座標
            z2 (int): 2つ目の座標のZ座標
            cord (str): 座標系 ("": 絶対座標, "~": 相対座標, "^": ローカル座標)
            
        Example:
            >>> # 絶対座標で領域を定義
            >>> Volume(100, 64, -200, 110, 70, -190)
            >>> # 相対座標で領域を定義
            >>> Volume(-5, -5, -5, 5, 5, 5, "~")
            >>> # ローカル座標で領域を定義
            >>> Volume(-5, -5, -5, 5, 5, 5, "^")
        """
        self.pos1 = (x1, y1, z1, cord)
        self.pos2 = (x2, y2, z2, cord)

class Entity:
    """
    エンティティを表すクラス

    :category: 基本クラス
    """
    def __init__(self, client: _WebSocketClient, world: str, uuid: str):
        self.client = client
        self.world = world
        self.uuid = uuid
        self.positions = []

    def reset(self):
        self.client.send_call(self.uuid, "restoreArea")

    def wait_for_player_chat(self) -> ChatMessage:
        """
        プレイヤーのチャットを待つ

        Returns:
            ChatMessage: チャットメッセージの情報
        """
        self.client.wait_for(self.uuid, "onPlayerChat")
        return ChatMessage(**json.loads(self.client.result))

    def wait_for_redstone_change(self) -> RedstonePower:
        """
        レッドストーン信号が変わるのを待つ

        Returns:
            RedstonePower: レッドストーン信号の情報
        """
        self.client.wait_for(self.uuid, "onEntityRedstone")
        return RedstonePower(**json.loads(self.client.result))

    def wait_for_block_break(self) -> Block:
        """
        ブロックが壊されるのを待つ

        Returns:
            Block: 壊されたブロックの情報
        """
        self.client.wait_for(self.uuid, "onBlockBreak")
        return Block(**json.loads(self.client.result))
    
    def get_event_message(self) -> Any:
        self.client.send_call(self.uuid, "getEventMessage")
        return json.loads(self.client.result)

    def is_event_area(self, loc: Location) -> bool:
        """
        指定された座標がイベント検出範囲内かどうかを判定する

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 指定された座標がイベント検出範囲内の場合はTrue、そうでない場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)がイベント検出範囲内かどうかを判定
                loc = LocationFactory.absolute(100, 64, -200)
                entity.is_event_area(loc)

            .. code-block:: python

                # 自分の東10ブロック、北5ブロックの位置がイベント検出範囲内かどうかを判定
                loc = LocationFactory.relative(10, 0, -5)
                entity.is_event_area(loc)

            .. code-block:: python

                # 自分の真上5ブロックの位置がイベント検出範囲内かどうかを判定
                loc = LocationFactory.local(0, 5, 0)
                entity.is_event_area(loc)
        """
        self.client.send_call(self.uuid, "isEventArea", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def set_event_area(self, volume: Volume) -> bool:
        """
        イベントの検出範囲を設定する

        Args:
            volume (Volume): イベントの検出範囲

        Returns:
            bool: 設定が成功した場合はTrue、失敗した場合はFalse

        Example:
            >>> # 絶対座標で領域を設定
            >>> entity.set_event_area(Volume.absolute(100, 64, -200, 110, 70, -190))
            >>> # 相対座標で領域を設定（自分の周囲10ブロック）
            >>> entity.set_event_area(Volume.relative(-5, -5, -5, 5, 5, 5))
            >>> # ローカル座標で領域を設定（自分の周囲10ブロック）
            >>> entity.set_event_area(Volume.local(-5, -5, -5, 5, 5, 5))
        """
        x1, y1, z1, cord = volume.pos1
        x2, y2, z2, _ = volume.pos2
        self.client.send_call(self.uuid, "setEventArea", [x1, y1, z1, x2, y2, z2, cord])
        return str_to_bool(self.client.result)

    def set_on_message(self, callback_func: Callable[['Entity', str], Any]):
        """
        カスタムイベントメッセージを受信したときに呼び出されるコールバック関数を設定する
        """
        def callback_wrapper(data):
            logging.debug("set_on_message callback_wrapper '%s'" % data)
            if(data['entityUuid'] == self.uuid):
                logging.debug("callback_wrapper '%s'" % data)
                event = EventMessage(**data)
                callback_func(self, event)
        self.client.set_callback('onCustomEvent', callback_wrapper)

    def send_message(self, target: str, message: str):
        """
        カスタムイベントメッセージを送信する

        Args:
            target (str): 送信先のEntityの名前
            message (str): 送信するメッセージの内容
        """
        self.client.send_call(self.uuid, "sendEvent", [target, message])

    def execute_command(self, command: str):
        """
        コマンドを実行する

        Args:
            command (str): 実行するコマンドの内容
        """
        self.client.send_call(self.uuid, "executeCommand", [command])
    
    def open_inventory(self, loc: Location) -> Inventory:
        """
        指定された座標のインベントリ（チェストなど）を開く

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            Inventory: 開いたインベントリの操作オブジェクト

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)のチェストを開く
                loc = LocationFactory.absolute(100, 64, -200)
                chest = entity.open_inventory(loc)

            .. code-block:: python

                # インベントリ内のアイテムを取得
                items = chest.get_all_items()

            .. code-block:: python

                # アイテムを移動
                chest.move_item(0, 1)
        """
        self.client.send_call(self.uuid, "openInventory", [loc.x, loc.y, loc.z, loc.cord])
        inventory = Inventory(self.client, self.uuid, ** json.loads(self.client.result))
        return inventory

    def push(self) -> bool:
        """
        自分の位置を保存する
        """
        pos = self.get_location()
        self.positions.append(pos)
        return True
    
    def pop(self) -> bool:
        """
        自分の位置を保存した位置に戻す
        """
        if(len(self.positions) > 0):
            pos = self.positions.pop()
            self.teleport(pos)
            return True
        else:
            return False

    def forward(self, n=1) -> bool:
        """
        n歩前に進む

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "forward", [n])
        return str_to_bool(self.client.result)

    def back(self, n=1) -> bool:
        """
        n歩後ろに進む

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "back", [n])
        return str_to_bool(self.client.result)

    def up(self, n=1) -> bool:
        """
        n歩上に進む

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "up", [n])
        return str_to_bool(self.client.result)

    def down(self, n=1) -> bool:
        """
        n歩下に進む

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "down", [n])
        return str_to_bool(self.client.result)

    def step_left(self, n=1) -> bool:
        """
        n歩左にステップする

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "stepLeft", [n])
        return str_to_bool(self.client.result)

    def step_right(self, n=1) -> bool:
        """
        n歩右にステップする

        Args:
            n (int, optional): 進む歩数. デフォルトは1.

        Returns:
            bool: 移動が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "stepRight", [n])
        return str_to_bool(self.client.result)

    def turn_left(self):
        """
        左に回転させる

        Returns:
            None
        """
        self.client.send_call(self.uuid, "turnLeft")

    def turn_right(self):
        """
        右に回転させる

        Returns:
            None
        """
        self.client.send_call(self.uuid, "turnRight")

    def make_sound(self) -> bool:
        """
        鳴かせる

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "sound")
        return str_to_bool(self.client.result)

    def add_force(self, x: float, y: float, z: float) -> bool:
        """
        エンティティに力を加えて移動させる

        Args:
            x (float): X軸方向の力（正の値で東方向、負の値で西方向）
            y (float): Y軸方向の力（正の値で上方向、負の値で下方向）
            z (float): Z軸方向の力（正の値で南方向、負の値で北方向）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 東方向に力を加える
                entity.add_force(1.0, 0.0, 0.0)

            .. code-block:: python

                # 上方向にジャンプするような力を加える
                entity.add_force(0.0, 1.0, 0.0)
        """
        self.client.send_call(self.uuid, "addForce", [x, y, z])
        return str_to_bool(self.client.result)

    def jump(self):
        """
        ジャンプさせる

        Returns:
            None
        """
        self.client.send_call(self.uuid, "jump")

    def turn(self, degrees: int):
        """
        エンティティを指定した角度だけ回転させる

        Args:
            degrees (int): 回転する角度（正の値で右回り、負の値で左回り）
                例: 90で右に90度回転、-90で左に90度回転

        Returns:
            None

        Example:
            .. code-block:: python

                # 右に90度回転
                entity.turn(90)

            .. code-block:: python

                # 左に180度回転
                entity.turn(-180)
        """
        self.client.send_call(self.uuid, "turn", [degrees])

    def facing(self, angle: int):
        """
        エンティティを指定した方角に向かせる

        Args:
            angle (int): 向く方角（度数法）
                - 0: 南
                - 90: 西
                - 180: 北
                - 270: 東

        Returns:
            None

        Example:
            .. code-block:: python

                # 北を向く
                entity.facing(180)

            .. code-block:: python

                # 東を向く
                entity.facing(270)
        """
        self.client.send_call(self.uuid, "facing", [angle])

    def place_at(self, loc: Location, side=None) -> bool:
        """
        指定した座標にブロックを設置する

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

            side (str, optional): ブロックを設置する面
                - Side.right: 右面
                - Side.left: 左面
                - Side.front: 前面
                - Side.back: 後面
                - Side.top: 上面
                - Side.bottom: 下面

                Noneの場合は自動的に適切な面を選択

        Returns:
            bool: 設置が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)にブロックを設置
                loc = LocationFactory.absolute(100, 64, -200)
                entity.place_at(loc)

            .. code-block:: python

                # 自分の東10ブロックの位置にブロックを右面に設置
                loc = LocationFactory.relative(10, 0, 0)
                entity.place_at(loc, Side.right)
        """
        self.client.send_call(self.uuid, "placeX", [loc.x, loc.y, loc.z, loc.cord, side])
        return str_to_bool(self.client.result)

    def place(self, side=None) -> bool:
        """
        自分の前方にブロックを設置する

        Args:
            side (str, optional): ブロックを設置する面
                - Side.right: 右面
                - Side.left: 左面
                - Side.front: 前面
                - Side.back: 後面
                - Side.top: 上面
                - Side.bottom: 下面

                Noneの場合は自動的に適切な面を選択

        Returns:
            bool: 設置が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 前方にブロックを設置
                entity.place()

            .. code-block:: python

                # 前方のブロックを右面に設置
                entity.place(Side.right)
        """
        self.client.send_call(self.uuid, "placeFront", [side])
        return str_to_bool(self.client.result)

    def place_up(self, side=None) -> bool:
        """
        自分の真上にブロックを設置する

        Args:
            side (str, optional): ブロックを設置する面
                - Side.right: 右面
                - Side.left: 左面
                - Side.front: 前面
                - Side.back: 後面
                - Side.top: 上面
                - Side.bottom: 下面

                Noneの場合は自動的に適切な面を選択

        Returns:
            bool: 設置が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 真上にブロックを設置
                entity.place_up()

            .. code-block:: python

                # 真上のブロックを上面に設置
                entity.place_up(Side.top)
        """
        self.client.send_call(self.uuid, "placeUp", [side])
        return str_to_bool(self.client.result)

    def place_down(self, side=None) -> bool:
        """
        自分の真下にブロックを設置する

        Args:
            side (str, optional): ブロックを設置する面
                - Side.right: 右面
                - Side.left: 左面
                - Side.front: 前面
                - Side.back: 後面
                - Side.top: 上面
                - Side.bottom: 下面

                Noneの場合は自動的に適切な面を選択

        Returns:
            bool: 設置が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 真下にブロックを設置
                entity.place_down()

            .. code-block:: python

                # 真下のブロックを下面に設置
                entity.place_down(Side.bottom)
        """
        self.client.send_call(self.uuid, "placeDown", [side])
        return str_to_bool(self.client.result)

    def use_item_at(self, loc: Location) -> bool:
        """
        指定した座標にアイテムを使う

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)でアイテムを使用
                loc = LocationFactory.absolute(100, 64, -200)
                entity.use_item_at(loc)

            .. code-block:: python

                # 自分の東10ブロック、北5ブロックの位置でアイテムを使用
                loc = LocationFactory.relative(10, 0, -5)
                entity.use_item_at(loc)

            .. code-block:: python

                # 自分の真上5ブロックの位置でアイテムを使用
                loc = LocationFactory.local(0, 5, 0)
                entity.use_item_at(loc)
        """
        self.client.send_call(self.uuid, "useItemX", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def use_item(self) -> bool:
        """
        自分の前方にアイテムを使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "useItemFront")
        return str_to_bool(self.client.result)

    def use_item_up(self) -> bool:
        """
        自分の真上にアイテムを使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "useItemUp")
        return str_to_bool(self.client.result)

    def use_item_down(self) -> bool:
        """
        自分の真下にアイテムを使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "useItemDown")
        return str_to_bool(self.client.result)

    def harvest(self) -> bool:
        """
        自分の位置または足元の作物を収穫する
        (0, 0, 0) または (0, -1, 0) の位置にある収穫可能な作物を自動的に収穫します

        Returns:
            bool: 収穫が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "harvest")
        return str_to_bool(self.client.result)

    def plant(self) -> bool:
        """
        自分の足元に作物を植える
        常に無限で、インベントリチェックなし
        (0, -1, 0) の位置にある耕地に作物を植えます

        Returns:
            bool: 植えるのが成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "plant")
        return str_to_bool(self.client.result)

    def fertilizer(self) -> bool:
        """
        自分の足元の作物に肥料（骨粉）を与える
        常に無限で、インベントリチェックなし
        (0, -1, 0) または (0, 0, 0) の位置にある作物に肥料を与えます

        Returns:
            bool: 肥料を与えるのが成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "fertilizer")
        return str_to_bool(self.client.result)

    def dig(self) -> bool:
        """
        自分の前方のブロックを壊す

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "digX", [0, 0, 1])
        return str_to_bool(self.client.result)

    def dig_up(self) -> bool:
        """
        自分の真上のブロックを壊す

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "digX", [0, 1, 0])
        return str_to_bool(self.client.result)

    def dig_down(self) -> bool:
        """
        自分の真下のブロックを壊す

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "digX", [0, -1, 0])
        return str_to_bool(self.client.result)

    # ===== Sign Operations =====

    def write_sign(self, text) -> bool:
        """
        自分の前方の看板にテキストを書き込む

        Args:
            text: 書き込むテキスト。文字列またはリスト（各要素が各行になる、最大4行）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse

        Examples:
            文字列で書き込む::

                entity.write_sign("Hello World")

            複数行を書き込む::

                entity.write_sign(["1行目", "2行目", "3行目", "4行目"])
        """
        if isinstance(text, list):
            text = '\n'.join(str(line) for line in text[:4])
        self.client.send_call(self.uuid, "setSign", [str(text), "front"])
        return str_to_bool(self.client.result)

    def write_sign_up(self, text) -> bool:
        """
        自分の真上の看板にテキストを書き込む

        Args:
            text: 書き込むテキスト。文字列またはリスト（各要素が各行になる、最大4行）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        if isinstance(text, list):
            text = '\n'.join(str(line) for line in text[:4])
        self.client.send_call(self.uuid, "setSign", [str(text), "up"])
        return str_to_bool(self.client.result)

    def write_sign_down(self, text) -> bool:
        """
        自分の真下の看板にテキストを書き込む

        Args:
            text: 書き込むテキスト。文字列またはリスト（各要素が各行になる、最大4行）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        if isinstance(text, list):
            text = '\n'.join(str(line) for line in text[:4])
        self.client.send_call(self.uuid, "setSign", [str(text), "down"])
        return str_to_bool(self.client.result)

    def write_sign_at(self, loc: Location, text) -> bool:
        """
        指定した座標の看板にテキストを書き込む

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）
            text: 書き込むテキスト。文字列またはリスト（各要素が各行になる、最大4行）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse

        Examples:
            相対座標で指定::

                loc = LocationFactory.relative(0, 1, 0)  # 1ブロック上
                entity.write_sign_at(loc, "相対座標のメッセージ")

            ローカル座標で指定::

                loc = LocationFactory.local(0, 0, 1)  # 前方1ブロック
                entity.write_sign_at(loc, "ローカル座標のメッセージ")

            複数行を書き込む::

                loc = LocationFactory.local(0, 0, 1)
                entity.write_sign_at(loc, ["1行目", "2行目", "3行目"])
        """
        if isinstance(text, list):
            text = '\n'.join(str(line) for line in text[:4])
        self.client.send_call(self.uuid, "setSignX", [str(text), loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def read_sign(self) -> str:
        """
        自分の前方の看板のテキストを読み取る

        Returns:
            str: 看板のテキスト（複数行の場合は改行で区切られた文字列）、看板がない場合は空文字列

        Examples:
            テキストを読み取る::

                text = entity.read_sign()
                print(text)  # "1行目\\n2行目\\n..."
        """
        self.client.send_call(self.uuid, "getSign", ["front"])
        return self.client.result if self.client.result else ""

    def read_sign_up(self) -> str:
        """
        自分の真上の看板のテキストを読み取る

        Returns:
            str: 看板のテキスト（複数行の場合は改行で区切られた文字列）、看板がない場合は空文字列
        """
        self.client.send_call(self.uuid, "getSign", ["up"])
        return self.client.result if self.client.result else ""

    def read_sign_down(self) -> str:
        """
        自分の真下の看板のテキストを読み取る

        Returns:
            str: 看板のテキスト（複数行の場合は改行で区切られた文字列）、看板がない場合は空文字列
        """
        self.client.send_call(self.uuid, "getSign", ["down"])
        return self.client.result if self.client.result else ""

    def read_sign_at(self, loc: Location) -> str:
        """
        指定した座標の看板のテキストを読み取る

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            str: 看板のテキスト（複数行の場合は改行で区切られた文字列）、看板がない場合は空文字列

        Examples:
            相対座標で指定::

                loc = LocationFactory.relative(0, 1, 0)  # 1ブロック上
                text = entity.read_sign_at(loc)

            ローカル座標で指定::

                loc = LocationFactory.local(0, 0, 1)  # 前方1ブロック
                text = entity.read_sign_at(loc)
        """
        self.client.send_call(self.uuid, "getSignX", [loc.x, loc.y, loc.z, loc.cord])
        return self.client.result if self.client.result else ""

    # ===== End Sign Operations =====

    def attack(self) -> bool:
        """
        自分の前方を攻撃する

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "attack")
        return str_to_bool(self.client.result)

    def plant_at(self, loc: Location) -> bool:
        """
        指定した座標のブロックに植物を植える

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "plantX", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def harvest_at(self, loc: Location) -> bool:
        """
        指定した座標の作物を収穫する
        常に無限で、インベントリチェックなし
        指定された位置にある収穫可能な作物を収穫します

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 収穫が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)の作物を収穫
                loc = LocationFactory.absolute(100, 64, -200)
                entity.harvest_at(loc)

            .. code-block:: python

                # 自分の足元の作物を収穫
                loc = LocationFactory.local(0, -1, 0)
                entity.harvest_at(loc)
        """
        self.client.send_call(self.uuid, "harvestAt", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def fertilizer_at(self, loc: Location) -> bool:
        """
        指定した座標の作物に肥料（骨粉）を与える
        常に無限で、インベントリチェックなし
        指定された位置にある作物に肥料を与えます

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 肥料を与えるのが成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)の作物に肥料を与える
                loc = LocationFactory.absolute(100, 64, -200)
                entity.fertilizer_at(loc)

            .. code-block:: python

                # 自分の足元の作物に肥料を与える
                loc = LocationFactory.local(0, -1, 0)
                entity.fertilizer_at(loc)
        """
        self.client.send_call(self.uuid, "fertilizerAt", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def till_at(self, loc: Location) -> bool:
        """
        指定した座標のブロックを耕す

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "tillX", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def flatten_at(self, loc: Location) -> bool:
        """
        指定した座標のブロックを平らにする

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "flattenX", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def dig_at(self, loc: Location) -> bool:
        """
        指定した座標のブロックを壊す

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)のブロックを壊す
                loc = LocationFactory.absolute(100, 64, -200)
                entity.dig_at(loc)

            .. code-block:: python

                # 自分の東10ブロック、北5ブロックの位置のブロックを壊す
                loc = LocationFactory.relative(10, 0, -5)
                entity.dig_at(loc)

            .. code-block:: python

                # 自分の真上5ブロックの位置のブロックを壊す
                loc = LocationFactory.local(0, 5, 0)
                entity.dig_at(loc)
        """
        self.client.send_call(self.uuid, "digX", [loc.x, loc.y, loc.z, loc.cord])
        return str_to_bool(self.client.result)

    def pickup_items_at(self, loc: Location) -> int:
        """
        指定した座標の周辺のアイテムを拾う

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            int: 拾ったアイテムの数
        """
        self.client.send_call(self.uuid, "pickupItemsX", [loc.x, loc.y, loc.z, loc.cord])
        return int(self.client.result)

    def action(self) -> bool:
        """
        自分の前方の装置を使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "actionFront")
        return str_to_bool(self.client.result)

    def action_up(self) -> bool:
        """
        自分の真上の装置を使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "actionUp")
        return str_to_bool(self.client.result)

    def action_down(self) -> bool:
        """
        自分の真下の装置を使う

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "actionDown")
        return str_to_bool(self.client.result)

    def set_item(self, slot: int, block: str) -> bool:
        """
        自分のインベントリの指定したスロットにアイテムを設定する

        Args:
            slot (int): 設定するスロット番号（0から始まる）
            block (str): 設定するブロックの種類（例: "stone", "dirt", "oak_planks"）
                データ値が必要な場合は "block:data" の形式で指定
                例: "stone:1"（花崗岩）, "wool:14"（赤の羊毛）

        Returns:
            bool: 設定が成功した場合はTrue、失敗した場合はFalse

        Example:
            .. code-block:: python

                # スロット0に石を設定
                entity.set_item(0, "stone")

            .. code-block:: python

                # スロット1に花崗岩を設定
                entity.set_item(1, "stone:1")
        """
        self.client.send_call(self.uuid, "setItem", [slot, block])
        return str_to_bool(self.client.result)

    def get_item(self, slot: int) -> ItemStack:
        """
        自分のインベントリからアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号
        """
        self.client.send_call(self.uuid, "getItem", [slot])
        item_stack = ItemStack(** json.loads(self.client.result))
        return item_stack

    def swap_item(self, slot1: int, slot2: int) -> bool:
        """
        自分のインベントリのアイテムを置き換える

        Args:
            slot1 (int): 入れ替え元のスロット番号
            slot2 (int): 入れ替え先のスロット番号

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "swapItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def move_item(self, slot1: int, slot2: int) -> bool:
        """
        自分のインベントリのアイテムを移動させる

        Args:
            slot1 (int): 移動元のスロット番号
            slot2 (int): 移動先のスロット番号

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "moveItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def drop_item(self, slot1: int) -> bool:
        """
        自分のインベントリのアイテムを落とす

        Args:
            slot1 (int): 落とすアイテムのスロット番号

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "dropItem", [slot1])
        return str_to_bool(self.client.result)

    def select_item(self, slot: int) -> bool:
        """
        自分のインベントリのアイテムを手に持たせる

        Args:
            slot (int): アイテムを持たせたいスロットの番号

        Returns:
            bool: 操作が成功した場合はTrue、失敗した場合はFalse
        """
        self.client.send_call(self.uuid, "grabItem", [slot])
        return str_to_bool(self.client.result)

    def say(self, message: str):
        """
        メッセージをチャットに送る

        Args:
            message (str): エンティティがチャットで送信するメッセージの内容

        Returns:
            None
        """
        self.client.send_call(self.uuid, "sendChat", [message])

    def find_nearby_block_at(self, loc: Location, block: str, max_depth: int) -> Optional[Block]:
        """
        指定された座標を中心に近くのブロックを取得する

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）
            block (str): ブロックの名前( "water:0" など)
            max_depth (int): 探索する最大の深さ

        Returns:
            Optional[Block]: 見つかったブロックの情報、見つからなかった場合はNone
        """
        self.client.send_call(self.uuid, "findNearbyBlockX", [loc.x, loc.y, loc.z, loc.cord, block, max_depth])
    
        print('result = ', self.client.result)
        if not self.client.result:
            return None
        
        try:
            result = json.loads(self.client.result)
            if not result:
                return None
        except json.JSONDecodeError:
            return None

        block = Block(**result)
        return block

    def inspect_at(self, loc: Location) -> Block:
        """
        指定された座標のブロックを調べる

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            Block: 調べたブロックの情報
        """
        self.client.send_call(self.uuid, "inspect", [loc.x, loc.y, loc.z, loc.cord])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect(self) -> Block:
        """
        自分の前方のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, 0, 1])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect_up(self) -> Block:
        """
        真上のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, 1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect_down(self) -> Block:
        """
        自分の足元のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, -1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def get_location(self) -> Location:
        """
        自分の現在位置を調べる
        Returns:
            Location: 調べた位置情報    
        """
        self.client.send_call(self.uuid, "getPosition")
        return Location(** json.loads(self.client.result))
    
    def teleport(self, loc: Location):
        """
        指定された座標に移動する

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            None
        """
        self.client.send_call(self.uuid, "teleport", [loc.x, loc.y, loc.z, loc.cord])

    def is_blocked(self) -> bool:
        """
        自分の前方にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedFront")
        return str_to_bool(self.client.result)

    def is_blocked_up(self) -> bool:
        """
        自分の真上にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedUp")
        return str_to_bool(self.client.result)

    def is_blocked_down(self) -> bool:
        """
        自分の真下にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedDown")
        return str_to_bool(self.client.result)

    def can_dig(self) -> bool:
        """
        自分の前方のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigFront")
        return str_to_bool(self.client.result)

    def can_dig_up(self) -> bool:
        """
        自分の上のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigUp")
        return str_to_bool(self.client.result)

    def can_dig_down(self) -> bool:
        """
        自分の下のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigDown")
        return str_to_bool(self.client.result)

    def get_distance(self) -> float:
        """
        自分と前方のなにかとの距離を調べる

        Returns:
            float: 前方の物体との距離
        """
        self.client.send_call(self.uuid, "getTargetDistanceFront")
        return float(self.client.result)

    def get_distance_up(self) -> float:
        """
        自分と真上のなにかとの距離を調べる

        Returns:
            float: 真上の物体との距離
        """
        self.client.send_call(self.uuid, "getTargetDistanceUp")
        return float(self.client.result)

    def get_distance_down(self) -> float:
        """
        自分と真下のなにかとの距離を調べる

        Returns:
            float: 真下の物体との距離
        """
        self.client.send_call(self.uuid, "getTargetDistanceDown")
        return float(self.client.result)

    def get_distance_target(self, uuid) -> float:
        """
        自分とターゲットとの距離を調べる

        Args:
            uuid (str): ターゲットのUUID

        Returns:
            float: ターゲットとの距離
        """
        self.client.send_call(self.uuid, "getTargetDistance", [uuid])
        return float(self.client.result)

    def get_block(self, loc: Location) -> Block:
        """
        指定した座標のブロック情報を取得する

        Args:
            loc (Location): 座標情報（LocationFactory.absolute/relative/localで生成）

        Returns:
            Block: ブロックの情報（種類、データ値、座標）

        Example:
            .. code-block:: python

                # 絶対座標(100, 64, -200)のブロック情報を取得
                loc = LocationFactory.absolute(100, 64, -200)
                block = entity.get_block(loc)
                print(f"ブロック: {block.name}, データ値: {block.data}")

            .. code-block:: python

                # 自分の東10ブロックの位置のブロック情報を取得
                loc = LocationFactory.relative(10, 0, 0)
                block = entity.get_block(loc)
                print(f"ブロック: {block.name}, データ値: {block.data}")
        """
        self.client.send_call(self.uuid, "getBlock", [loc.x, loc.y, loc.z, loc.cord])
        block = Block(** json.loads(self.client.result))
        return block

    def get_block_by_name(self, name: str) -> Block:
        """
        指定された名前のブロックを取得する

        Args:
            name (str): ブロックの名前（例: "stone", "dirt", "oak_planks"）
                データ値が必要な場合は "block:data" の形式で指定
                例: "stone:1"（花崗岩）, "wool:14"（赤の羊毛）

        Returns:
            Block: 指定された名前のブロックの情報

        Example:
            .. code-block:: python

                # 石ブロックを取得
                block = entity.get_block_by_name("stone")
                print(f"ブロック: {block.name}, データ値: {block.data}")

            .. code-block:: python

                # 花崗岩を取得
                block = entity.get_block_by_name("stone:1")
                print(f"ブロック: {block.name}, データ値: {block.data}")
        """
        self.client.send_call(self.uuid, "blockName", [name])
        block = Block(** json.loads(self.client.result))
        return block

    def get_block_by_color(self, color: str) -> Block:
        """
        指定された色に最も近いブロックを取得する

        Args:
            color (str): ブロックの色（HexRGB形式、例: "#FF0000"で赤）
                色は16進数のRGB値で指定（#RRGGBB形式）

        Returns:
            Block: 指定された色に最も近いブロックの情報

        Example:
            .. code-block:: python

                # 赤色に近いブロックを取得
                block = entity.get_block_by_color("#FF0000")
                print(f"ブロック: {block.name}, データ値: {block.data}")

            .. code-block:: python

                # 青色に近いブロックを取得
                block = entity.get_block_by_color("#0000FF")
                print(f"ブロック: {block.name}, データ値: {block.data}")
        """
        self.client.send_call(self.uuid, "blockColor", [color])
        block = Block(** json.loads(self.client.result))
        return block

    def _convert_recipe_pattern(self, recipe):
        """
        Convert recipe pattern to comma-separated string format.

        Handles two input formats:
        1. String: "1,1,1,,2,,,2" -> returns as-is
        2. List: [1,1,1,None,2,None,None,2] -> "1,1,1,,2,,,2"

        Args:
            recipe: Recipe pattern as string or list

        Returns:
            str: Comma-separated string pattern

        Raises:
            ValueError: If pattern is invalid
        """
        # If already a string, validate and return
        if isinstance(recipe, str):
            if not recipe.strip():
                raise ValueError("Pattern cannot be empty")

            elements = recipe.split(",")
            if len(elements) > 9:
                raise ValueError(f"Pattern exceeds 3x3 grid size (max 9 elements, got {len(elements)})")

            # Validate each non-empty element is a valid number or 'X'
            for i, element in enumerate(elements):
                trimmed = element.strip()
                if trimmed:
                    # Allow 'X' or 'x' as AIR placeholder
                    if trimmed.upper() == 'X':
                        continue
                    try:
                        int(trimmed)
                        # Allow any integer (negative values are treated as AIR on server)
                    except ValueError as e:
                        if "invalid literal" in str(e):
                            raise ValueError(f"Invalid slot number at position {i}: '{element}' (use number or 'X' for empty)")
                        raise

            return recipe

        # List format
        if isinstance(recipe, list):
            if len(recipe) == 0:
                raise ValueError("Pattern list cannot be empty")

            if len(recipe) > 9:
                raise ValueError(f"Pattern exceeds 3x3 grid size (max 9 elements, got {len(recipe)})")

            # Validate and convert to string
            result = []
            for i, slot in enumerate(recipe):
                if slot is None or slot == "":
                    result.append("")
                elif isinstance(slot, str):
                    # Allow 'X' or 'x' as AIR placeholder, convert to -1
                    if slot.strip().upper() == 'X':
                        result.append("-1")
                    else:
                        raise ValueError(f"Invalid slot value at position {i}: '{slot}' (use number, None, or 'X')")
                elif isinstance(slot, int):
                    # Allow any integer (negative values are treated as AIR on server)
                    result.append(str(slot))
                else:
                    raise ValueError(f"Invalid slot value at position {i}: {slot}")

            return ",".join(result)

        raise ValueError("Recipe pattern must be a string or list")

    def craft(self, recipe, qty=1, slot=None):
        """
        ペットのインベントリにある材料を使ってアイテムをクラフトする。

        引数:
            recipe: レシピパターン（文字列またはリスト形式）
                - 文字列形式: "1,1,1,X,2,X,X,2,X" （カンマ区切りのスロット番号、空は X または空文字）
                - リスト形式: [1,1,1,"X",2,"X","X",2,"X"] または [1,1,1,None,2,None,None,2,None]
                - スロット番号は0から始まる（0=スロット1）
                - 負の数(-1など)も空気として扱われる
            qty: クラフトする個数（デフォルト: 1）
            slot: 結果を配置するスロット番号（デフォルト: None = 自動配置）

        戻り値:
            dict: クラフト結果（以下の構造）
                {
                    "success": bool,              # 成功したか
                    "result_item": str | None,    # 作成されたアイテム名
                    "result_quantity": int | None,# 作成された個数
                    "requested_quantity": int,    # リクエストした個数
                    "result_slot": int | None,    # 配置されたスロット
                    "materials_consumed": dict,   # 消費された材料
                    "game_mode": str,             # ゲームモード
                    "error": dict | None          # エラー情報
                }

        使用例:
            >>> # パンをクラフト（スロット0に小麦3つ）
            >>> result = entity.craft("0,0,0")
            >>> if result["success"]:
            >>>     print(f"{result['result_item']}を{result['result_quantity']}個作ったよ！")

            >>> # リスト形式でつるはしをクラフト
            >>> result = entity.craft([3,3,3,"X",4,"X","X",4,"X"])

            >>> # 複数個クラフトして、スロット10に配置
            >>> result = entity.craft("0,0,0", qty=5, slot=10)

            >>> # エラー処理
            >>> result = entity.craft("0,0,0")
            >>> if not result["success"]:
            >>>     error = result["error"]
            >>>     print(f"エラー: {error['message']}")
            >>>     if error["code"] == "INSUFFICIENT_MATERIALS":
            >>>         print("材料が足りないよ")
        """
        # Convert recipe to string format
        pattern = self._convert_recipe_pattern(recipe)

        # Prepare arguments
        args = [pattern, qty]
        if slot is not None:
            args.append(slot)

        # Send craft request
        self.client.send_call(self.uuid, "craft", args)

        # Parse response
        result = json.loads(self.client.result)

        return result

    # ===== Livestock Methods =====

    def livestock_count_nearby(self, animal_type: str = "ALL", radius: float = 50.0) -> int:
        """
        近くの動物を数える
        
        Args:
            animal_type (str): 動物種別（COW, PIG, SHEEP, CHICKEN, RABBIT, HORSE, ALL）
            radius (float): 検索半径（ブロック数）
            
        Returns:
            int: 動物の数
            
        Example:
            >>> count = entity.livestock_count_nearby("COW", 50)
            >>> print(f"Found {count} cows")
        """
        self.client.send_call(self.uuid, "livestockCountNearby", [animal_type, radius])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Livestock operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {}).get('count', 0)

    def livestock_get_nearest_uuid(self, animal_type: str = "ALL", radius: float = 50.0) -> Optional[str]:
        """
        最も近い動物のUUIDを取得
        
        Args:
            animal_type (str): 動物種別（COW, PIG, SHEEP, CHICKEN, RABBIT, HORSE, ALL）
            radius (float): 検索半径（ブロック数）
            
        Returns:
            Optional[str]: 動物のUUID（見つからない場合はNone）
            
        Example:
            >>> cow_uuid = entity.livestock_get_nearest_uuid("COW", 50)
            >>> if cow_uuid:
            >>>     print(f"Found cow: {cow_uuid}")
        """
        self.client.send_call(self.uuid, "livestockGetNearestUuid", [animal_type, radius])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Livestock operation failed: {result.get('message', 'Unknown error')}")
        uuid = result.get('data', {}).get('uuid')
        return uuid if uuid else None

    def livestock_find_nearby(self, animal_type: str = "ALL", radius: float = 50.0) -> list:
        """
        近くの動物を詳細情報付きで検索
        
        Args:
            animal_type (str): 動物種別（COW, PIG, SHEEP, CHICKEN, RABBIT, HORSE, ALL）
            radius (float): 検索半径（ブロック数）
            
        Returns:
            list: 動物情報の辞書リスト
            
        Example:
            >>> animals = entity.livestock_find_nearby("SHEEP", 30)
            >>> for animal in animals:
            >>>     print(f"{animal['animalType']} at distance {animal['distance']}")
        """
        self.client.send_call(self.uuid, "livestockFindNearby", [animal_type, radius])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Livestock operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {}).get('entities', [])

    def livestock_herd(self, animal_uuid: str, x: float, y: float, z: float, cord: str = "^", speed: float = 1.0) -> None:
        """
        動物を指定座標に誘導

        Args:
            animal_uuid (str): 動物のUUID
            x (float): 目標X座標
            y (float): 目標Y座標
            z (float): 目標Z座標
            cord (str): 座標系（"": 絶対座標, "~": 相対座標, "^": ローカル座標、デフォルト: "^"）
            speed (float): 移動速度（0.5-2.0、デフォルト1.0）

        Example:
            >>> entity.livestock_herd(cow_uuid, 100, 64, 200, "^", 1.0)
        """
        self.client.send_call(self.uuid, "livestockHerd", [animal_uuid, x, y, z, cord, speed])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Herd operation failed: {result.get('message', 'Unknown error')}")

    def livestock_herd_all_nearby(
        self, 
        animal_type: str, 
        radius: float, 
        x: float, 
        y: float, 
        z: float, 
        cord: str = "^",
        speed: float = 1.0
    ) -> int:
        """
        近くの動物すべてを指定座標に誘導
        
        Args:
            animal_type (str): 動物種別（COW, PIG, SHEEP, CHICKEN, RABBIT, HORSE, ALL）
            radius (float): 検索半径（ブロック数）
            x (float): 目標X座標
            y (float): 目標Y座標
            z (float): 目標Z座標
            cord (str): 座標系（"": 絶対座標, "~": 相対座標, "^": ローカル座標、デフォルト: "^"）
            speed (float): 移動速度（0.5-2.0、デフォルト1.0）
            
        Returns:
            int: 誘導した動物の数
            
        Example:
            >>> count = entity.livestock_herd_all_nearby("COW", 50, 100, 64, 200)
            >>> print(f"Herded {count} cows")
        """
        self.client.send_call(self.uuid, "livestockHerdAllNearby", [animal_type, radius, x, y, z, cord, speed])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Herd all operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {}).get('count', 0)

    def livestock_shear(self, sheep_uuid: str) -> dict:
        """
        羊の毛を刈る
        
        Args:
            sheep_uuid (str): 羊のUUID
            
        Returns:
            dict: 羊毛情報 {wool, color, amount}
            
        Raises:
            Exception: 羊毛が生えていない、または羊以外の動物の場合
            
        Example:
            >>> try:
            >>>     result = entity.livestock_shear(sheep_uuid)
            >>>     print(f"Got {result['amount']} {result['color']} wool")
            >>> except Exception as e:
            >>>     print(f"Cannot shear: {e}")
        """
        self.client.send_call(self.uuid, "livestockShear", [sheep_uuid])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Shear operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {})

    def livestock_milk(self, cow_uuid: str) -> dict:
        """
        牛のミルクを搾る
        
        Args:
            cow_uuid (str): 牛のUUID
            
        Returns:
            dict: ミルク情報 {milk, amount}
            
        Raises:
            Exception: 牛以外の動物の場合
            
        Example:
            >>> try:
            >>>     result = entity.livestock_milk(cow_uuid)
            >>>     print(f"Got {result['amount']} milk bucket")
            >>> except Exception as e:
            >>>     print(f"Cannot milk: {e}")
        """
        self.client.send_call(self.uuid, "livestockMilk", [cow_uuid])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Milk operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {})

    def livestock_feed(self, animal_uuid: str, food_type: str = "wheat") -> None:
        """
        動物に餌をやる
        
        Args:
            animal_uuid (str): 動物のUUID
            food_type (str): 餌種別（wheat, carrot, seeds, beetroot）
            
        Example:
            >>> entity.livestock_feed(cow_uuid, "wheat")
        """
        self.client.send_call(self.uuid, "livestockFeed", [animal_uuid, food_type])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Feed operation failed: {result.get('message', 'Unknown error')}")

    def livestock_get_info(self, animal_uuid: str) -> dict:
        """
        動物の詳細情報を取得
        
        Args:
            animal_uuid (str): 動物のUUID
            
        Returns:
            dict: 動物の詳細情報
            
        Example:
            >>> info = entity.livestock_get_info(cow_uuid)
            >>> print(f"Health: {info['health']}/{info['maxHealth']}")
            >>> print(f"Can breed: {info['canBreed']}")
        """
        self.client.send_call(self.uuid, "livestockInfo", [animal_uuid])
        result = json.loads(self.client.result)
        if not result.get('success', False):
            raise Exception(f"Get info operation failed: {result.get('message', 'Unknown error')}")
        return result.get('data', {}).get('entityInfo', {})
