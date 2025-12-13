import requests
import socketio
import uuid
import threading
import time
import inspect
class Context:
    def __init__(self, bot, chat_id, message):
        self.bot = bot
        self.chat_id = chat_id
        self.message = message

    def send(self, text: str, buttons: list = None):
        keyboard = []
        if buttons:
            for row in buttons:
                keyboard_row = []
                for btn in row:
                    btn_data = {"text": btn.get("text", "Button")}
                    if "url" in btn:
                        btn_data["url"] = btn["url"]
                        btn_data["style"] = btn.get("style", "link")
                    elif "func" in btn and callable(btn["func"]):
                        cb_id = self.bot.register_callback(btn["func"])
                        btn_data["callbackData"] = cb_id
                        btn_data["style"] = btn.get("style", "primary")
                    elif "callback_data" in btn:
                        btn_data["callbackData"] = btn["callback_data"]
                        btn_data["style"] = btn.get("style", "primary")
                    
                    keyboard_row.append(btn_data)
                keyboard.append(keyboard_row)
        final_keyboard = keyboard if keyboard else None
        self.bot.send_message(self.chat_id, text, keyboard=final_keyboard)
    def start_typing(self):
        try:
            self.bot.socket.emit("typing", self.chat_id)
        except Exception as e:
            print(f"[AstrixRU] Ошибка start_typing: {e}. Бот будет вечно печатать! Обратитесь в поддержку: @itsoffkey")

    def stop_typing(self):
        try:
            self.bot.socket.emit("stop_typing", self.chat_id)
        except Exception as e:
            print(f"[AstrixRU] Ошибка stop_typing: {e}. Бот будет вечно печатать! Обратитесь в поддержку: @itsoffkey")
    def delete_message(self, message_timestamp: str):
        self.bot.delete_message(self.chat_id, message_timestamp)
    def react(self, message_timestamp: str, emoji: str):
        self.bot.react_to_message(self.chat_id, message_timestamp, emoji)

    def pin(self, message_timestamp: str):
        self.bot.pin_message(self.chat_id, message_timestamp)

    def unpin(self, message_timestamp: str):
        self.bot.unpin_message(self.chat_id, message_timestamp)

    def edit(self, message_timestamp: str, new_text: str):
        self.bot.edit_message(self.chat_id, message_timestamp, new_text)
    def send_modal(self, target_nickname: str, elements: list,
                   text: str = "", button_text: str = "OK",
                   input_placeholder: str = "", modal_id: str = None,
                   callback_to: str = None):
        if not self.bot.session_token:
            print("[Ошибка] Бот не авторизован.")
            return None
        normalized_elements = []
        if all(isinstance(e, str) for e in elements):
            normalized_elements = elements
        else:
            for el in elements:
                if not isinstance(el, dict):
                    continue
                t = el.get("type", "").lower()
                if t in ("text", "description", "label"):
                    if "text" and not text:
                        text = el.get("text") or el.get("label") or text
                    if 'text' not in normalized_elements:
                        normalized_elements.append('text')
                elif t in ("input", "textinput", "field"):
                    if el.get("placeholder") and not input_placeholder:
                        input_placeholder = el.get("placeholder")
                    if 'input' not in normalized_elements:
                        normalized_elements.append('input')
                elif t in ("button", "action"):
                    if el.get("buttonText") and not button_text:
                        button_text = el.get("buttonText")
                    if 'button' not in normalized_elements:
                        normalized_elements.append('button')
                else:
                    if el.get("label") or el.get("text"):
                        if 'text' not in normalized_elements:
                            normalized_elements.append('text')
        if not normalized_elements:
            normalized_elements = ['text', 'input', 'button']
    
        url = f"{self.bot.api_url}/api/bot/send-modal"
        payload = {
            "targetNickname": target_nickname,
            "elements": normalized_elements,
            "text": text or "",
            "buttonText": button_text or "OK",
            "inputPlaceholder": input_placeholder or "",
            "modalId": modal_id
        }
    
        headers = {
            "sessiontoken": self.bot.session_token,
            "Content-Type": "application/json"
        }
    
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 401:
                print("[Ошибка] Нужна авторизация (бот не распознан)")
                return None
    
            response.raise_for_status()
            data = response.json()
    
            if data.get("success"):
                print(f"[Модалка] Успешно отправил модалку пользователю {target_nickname}! (элементы={normalized_elements})")
            else:
                print(f"[Модалка] Ошибка отправления модалки.", data)
    
            return data
    
        except Exception as e:
            print(f"[Модалка] Ошибка при отправлении модалки: {e}. Не пробуйте решить это самостоятельно! Обратитесь в поддержку: @itsoffkey")
            return None
class AstrixBot:
    def __init__(self, token: str, api_url: str = "http://localhost:3000"):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.session_token = None
        self.bot_nickname = None
        self.socket = socketio.Client()
        self.joined_chats = set()
        self.callback_handlers = {}
        self.commands = {}
        self.socket.on("connect", self._on_connect)
        self.socket.on("disconnect", self._on_disconnect)
        self.socket.on("connect_error", self._on_connect_error)
        self.socket.on("new_message", self._on_new_message)
        self.socket.on("wallet_updated", self._on_wallet_updated)
        self.socket.on("interaction", self._on_interaction)
        self.socket.on("friend_request_received", self._on_friend_request_received)
    def login(self):
        print("[BOT] Starting...")
        res = requests.post(
            f"{self.api_url}/api/bot/login",
            json={"token": self.token},
            headers={"Content-Type": "application/json"},
        )
        if not res.ok:
            raise Exception(f"[Critical] Не удалось войти: {res.text} Бот отключен.")

        data = res.json()
        self.session_token = data.get("sessionToken")
        self.bot_nickname = data.get("bot", {}).get("name")
        if not self.session_token:
            raise Exception("[AstrixRU] Внимание!!! Боту не удалось получить sessionToken из API. ВАШ БОТ НЕ БУДЕТ РАБОТАТЬ! Обратитесь в поддержку для дальнейшей помощи: @itsoffkey (телеграм)")
            
        print("[BOT] Авторизация успешна!")
        print(f"[BOT] Никнейм бота: {self.bot_nickname}")
        if self.commands:
            commands_data = {}
            for cmd_name, cmd_data in self.commands.items():
                commands_data[cmd_name] = {
                    'description': cmd_data['description']
                }
            
            try:
                res = requests.post(
                    f"{self.api_url}/api/bot/update",
                    headers={
                        "sessiontoken": self.session_token,
                        "Content-Type": "application/json"
                    },
                    json={"commands": commands_data},
                    timeout=10
                )
                
                if not res.ok:
                    print(f"[Warning] Боту не удалось обновить команды: {res.status_code}. Это не так критично, но ваши команды не будут отображаться в чате. При этом ваши команды будут все также работать.")
                    if res.text:
                        print(f"[Info] Было обнаружено еще немного деталей: {res.text}")
                else:
                    print("[BOT] Команды успешно обновлены!")
                    print(f"[BOT] Я зарегистрировал {len(commands_data)} команд")
            except Exception as e:
                print(f"[BOT] Warning: Failed to update bot commands. Error: {str(e)}")
    def connect(self):
        print("[BOT] Подключение к серверам AstrixRU...")
        self.socket.connect(
            self.api_url,
            transports=["websocket"],
            auth={
                "nickname": self.bot_nickname,
                "sessionToken": self.session_token,
            },
        )

    def run_forever(self):
        print("[BOT] Бот успешно запущен и не будет остановлен до тех пор, пока вы не нажмете CTRL + C одновременно.")
        self._check_pending_requests()
        while True:
            time.sleep(1)
    def _on_connect(self):
        print("[BOT] Подключен к серверам AstrixRU!")

    def _on_disconnect(self):
        print("[BOT] Отключен от серверов AstrixRU!!! Это критично!! Бот будет пытаться переподключиться, и в данный момент он недоступен на сервисах AstrixRU.")

    def _on_connect_error(self, err):
        print(f"[BOT] Ошибка подключения: {err}. Не стоит разбираться самому, а лучше обратиться к специалистам, кто действительно разбирается в AstrixRU. Телеграм для связи: @itsoffkey.")
    def newCommand(self, command_name, description=""):
        def decorator(func):
            self.commands[command_name] = {
                'func': func,
                'description': description
            }
            return func

        return decorator
    def register_callback(self, func):
        cb_id = f"cb_{uuid.uuid4().hex[:12]}"
        self.callback_handlers[cb_id] = func
        return cb_id
    def _on_interaction(self, data):
        try:
            cb_id = data.get("callbackData")
            if cb_id in self.callback_handlers:
                func = self.callback_handlers[cb_id]
                chat_id = data.get("chatId")
                from_user = data.get("fromUser")
                sig = inspect.signature(func)
                params_count = len(sig.parameters)
                if params_count == 0:
                    func()
                elif params_count == 1:
                    func(chat_id)
                else:
                    func(chat_id, from_user)
            else:
                pass 
        except Exception as e:
            print(f"[Ошибка] Ошибка в интеракции: {e}. Обратитесь в поддержку: @itsoffkey")
    def _on_new_message(self, message):
        if not message or "chatId" not in message or "text" not in message:
            return
        if message.get("sender") == self.bot_nickname:
            return
        chat_id = message["chatId"]
        text = message["text"].strip()
        parts = text.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]
        if chat_id not in self.joined_chats:
            self.join_chat(chat_id)
        if cmd in self.commands:
            ctx = Context(self, chat_id, message)
            try:
                command = self.commands[cmd]
                func = command['func']
                sig = inspect.signature(func)
                if any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values()):
                    func(ctx, *args)
                else:
                    func(ctx, *args[: len(sig.parameters) - 1])
            except Exception as e:
                print(f"Error: {e}")
    def join_chat(self, chat_id):
        self.socket.emit("join_chat", chat_id)
        self.joined_chats.add(chat_id)
        print(f"[БОТ] Зашел в чат: {chat_id}")

    def send_message(self, chat_id, text, keyboard=None):
        payload = {
            "chatId": chat_id, 
            "id": str(uuid.uuid4()), 
            "text": text
        }
        
        if keyboard:
            payload["keyboard"] = keyboard
        self.socket.emit(
            "send_message",
            payload,
            callback=self._on_send_callback,
        )

    def _on_send_callback(self, callback):
        if not callback or not callback.get("success"):
            print("[AstrixRU] Ошибка при отправлении сообщения:", callback.get("error"))

    def get_conversations(self):
        if not self.session_token:
            print("[Ошибка] Бот не авторизован.")
            return None
    
        url = f"{self.api_url}/api/bot/conversations"
        try:
            response = requests.get(url, headers={"sessiontoken": self.session_token})
            if response.status_code == 401:
                print("[Ошибка] Нужна авторизация (бот не распознан)")
                return None
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                return data["conversations"]
            else:
                print("[AstrixRU] Ошибка при получении чатов:", data)
                return None
        except Exception as e:
            print(f"[AstrixRU] Ошибка при запросе к /api/conversations: {e}")
            return None
    def find_user(self, nickname: str):
        url = f"{self.api_url}/api/profile/{nickname}"
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"})
            if not response.ok:
                print(f"[AstrixRU] Ошибка при поиске пользователя {nickname}: {response.status_code}")
                return None
    
            data = response.json()
            if not data.get("success"):
                return None
    
            profile = data.get("profile")
            return profile
    
        except Exception as e:
            print(f"[AstrixRU] Ошибка при запрашивании профиля {nickname}: {e}")
            return None
    def get_music(self, page: int = 1, query: str = None):
        if not self.session_token:
            print("[Ошибка] Бот не авторизирован.")
            return None
    
        url = f"{self.api_url}/api/bot/music/list?page={page}"
        if query:
            url += f"&query={query}"
    
        try:
            headers = {
                "sessiontoken": self.session_token,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
    
            if response.status_code == 401:
                print("[Ошибка] Нужна авторизация (бот не распознан)")
                return None
    
            response.raise_for_status()
            data = response.json()
    
            if not data.get("success"):
                print("[AstrixRU] Ошибка получения музыки:", data)
                return None
    
            tracks = data.get("tracks", [])
            has_next = data.get("hasNextPage", False)
    
            music_list = []
            for track in tracks:
                music_list.append({
                    "id": track.get("id"),
                    "title": track.get("title"),
                    "artist": track.get("artist"),
                    "url": track.get("url"),
                    "uploader": track.get("uploader"),
                    "uploadDate": track.get("uploadDate")
                })
    
            return {
                "music": music_list,
                "has_next": has_next
            }
    
        except Exception as e:
            print(f"[AstrixRU] Ошибка получения музыки: {e}")
            return None
    def delete_message(self, chat_id: str, message_timestamp: str):
        try:
            self.socket.emit(
                "delete_message",
                {"chatId": chat_id, "messageTimestamp": message_timestamp},
                callback=self._on_delete_callback,
            )
        except Exception as e:
            print(f"[AstrixRU] Ошибка при удалении сообщения: {e}")

    def _on_delete_callback(self, callback):
        if not callback or not callback.get("success"):
            print("[AstrixRU] Ошибка при удалении сообщения:", callback.get("error"))

    def react_to_message(self, chat_id: str, message_timestamp: str, emoji: str):
        try:
            self.socket.emit(
                "react_to_message",
                {
                    "chatId": chat_id,
                    "messageTimestamp": message_timestamp,
                    "emoji": emoji,
                },
                callback=self._on_react_callback,
            )
        except Exception as e:
            print(f"[AstrixRU] Ошибка при добавлении реакции к сообщению: {e}")

    def _on_react_callback(self, callback):
        if not callback or not callback.get("success"):
            print("[AstrixRU] Ошибка при добавлении реакции к сообщению:", callback.get("error"))

    def pin_message(self, chat_id: str, message_timestamp: str):
        try:
            self.socket.emit(
                "pin_message",
                {"chatId": chat_id, "messageTimestamp": message_timestamp},
                callback=self._on_pin_callback,
            )
        except Exception as e:
            print(f"[AstrixRU] Ошибка при закреплении сообщения: {e}")

    def unpin_message(self, chat_id: str, message_timestamp: str):
        try:
            self.socket.emit(
                "unpin_message",
                {"chatId": chat_id, "messageTimestamp": message_timestamp},
                callback=self._on_pin_callback,
            )
        except Exception as e:
            print(f"[AstrixRU] Ошибка при закреплении сообщения: {e}")

    def _on_pin_callback(self, callback):
        if not callback or not callback.get("success"):
            print("[Бот] Ошибка при откреплении/закреплении сообщения:", callback.get("error"))
        else:
            print("[Бот] Сообщение успешно закреплено/откреплено.")

    def edit_message(self, chat_id: str, message_timestamp: str, new_text: str):
        try:
            self.socket.emit(
                "edit_message",
                {
                    "chatId": chat_id,
                    "messageTimestamp": message_timestamp,
                    "newText": new_text,
                },
                callback=self._on_edit_callback,
            )
        except Exception as e:
            print(f"[AstrixRU] Ошибка при редактировании сообщения: {e}. Обратитесь в поддержку: @itsoffkey")

    def _on_edit_callback(self, callback):
        if not callback or not callback.get("success"):
            print("[AstrixRU] Ошибка при редактировании сообщения:", callback.get("error"))

    def _on_wallet_updated(self, data):
        new_balance = data.get('newBalance')
        message = data.get('message')
        sender_info = data.get('senderInfo', {})
        amount = data.get('amount')
        if hasattr(self, 'on_wallet_updated') and callable(self.on_wallet_updated):
            try:
                self.on_wallet_updated(
                    new_balance=new_balance,
                    message=message,
                    sender_info=sender_info,
                    amount=amount
                )
            except Exception as e:
                print(f"[AstrixRU] Ошибка в обработчике on_wallet_updated: {e}")

    def _on_friend_request_received(self, data):
        sender_nickname = data.get("nickname")
        if sender_nickname:
            print(f"[BOT] Получена заявка в друзья от {sender_nickname}")
            self.accept_request(sender_nickname)

    def _check_pending_requests(self):
        if not self.session_token:
            return
        print("[BOT] Проверяю заявки в друзья... Это может занять несколько секунд.")
        try:
            headers = {"sessiontoken": self.session_token}
            res = requests.get(f"{self.api_url}/api/friends/list", headers=headers)
            if not res.ok:
                print(f"[AstrixRU] Внимание! Не удалось проверить список друзей. Статус код: {res.status_code}\nЧто это может означать?\nЕсли ваш бот был выключен, а вам кто то отправил заявки в друзья, бот НЕ сможет их принять.\nПожалуйста, отправьте данную ошибку в телеграм: @itsoffkey")
                return
            data = res.json()
            requests_list = data.get("requestsReceived", [])
            if not requests_list:
                print("[BOT] Нет никаких запросов в друзья.")
                return
            print(f"[BOT] Нашел {len(requests_list)} запросов в друзья. Обрабатываю...")
            for req in requests_list:
                self.accept_request(req["nickname"])
                time.sleep(0.5) 

        except Exception as e:
            print(f"[AstrixRU] Внимание! Не удалось проверить список друзей. Ошибка: {e}\nПожалуйста, напишите нам в телеграм для дальнейшей помощи: @itsoffkey")

    def accept_request(self, target_nickname: str):
        if not self.session_token:
            return
        try:
            url = f"{self.api_url}/api/friends/accept-request"
            headers = {
                "sessiontoken": self.session_token,
                "Content-Type": "application/json"
            }
            payload = {"senderNickname": target_nickname}
            res = requests.post(url, headers=headers, json=payload)
            if res.ok:
                print(f"[BOT] Заявка от {target_nickname} принята.")
            else:
                print(f"[BOT] Не удалось принять заявку от {target_nickname}: {res.text}")
        except Exception as e:
            print(f"[BOT] Error accepting request: {e}")