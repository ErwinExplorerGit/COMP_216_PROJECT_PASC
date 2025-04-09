import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from messages.alert import show_error
import threading

client = None
is_connected = False

topic_entry = None
message_entry = None
text_area = None
start_button = None
send_button = None


def on_connect(client, userdata, flags, rc, properties=None):
    if text_area:
        log("Connected to server.")


def log(msg):
    text_area.configure(state="normal")
    text_area.insert(tk.END, f"{msg}\n")
    text_area.configure(state="disabled")
    text_area.see(tk.END)


def connect_mqtt(client_id):
    global client, is_connected

    client = mqtt.Client(client_id=client_id,
                         callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    try:
        client.connect("localhost", 1883)
        client.loop_start()
        is_connected = True
        update_ui_state(connected=True)
    except Exception as e:
        show_error(f"Failed to connect: {e}")


def disconnect_mqtt():
    global is_connected
    if client:
        client.loop_stop()
        client.disconnect()
        is_connected = False
        update_ui_state(connected=False)
        topic_entry.delete(0, tk.END)
        clear_log()


def handle_start():
    if not is_connected:
        client_id = topic_entry.get().strip()
        if not client_id:
            show_error("Please enter a topic to use as client ID.")
            return
        threading.Thread(target=lambda: connect_mqtt(client_id)).start()
    else:
        disconnect_mqtt()


def send_message():
    if not is_connected:
        show_error("Please start the connection before sending messages.")
        return

    topic = topic_entry.get().strip()
    message = message_entry.get().strip()

    if not message:
        show_error("Message cannot be empty.")
        return

    client.publish(topic, message)
    log(f"Posted to '{topic}': {message}")
    print(f"Your '{message}' has been posted to the server!")

    message_entry.delete(0, tk.END)


def update_ui_state(connected):
    if connected:
        message_entry.config(state="normal")
        send_button.config(state="normal")
        topic_entry.config(state="readonly")
        start_button.config(text="Disconnect")
    else:
        message_entry.config(state="disabled")
        send_button.config(state="disabled")
        topic_entry.config(state="normal")
        start_button.config(text="Start")


def clear_log():
    text_area.configure(state="normal")
    text_area.delete("1.0", tk.END)
    text_area.configure(state="disabled")


def create_publisher_one(parent):
    global topic_entry, message_entry, text_area, start_button, send_button

    frame = tk.Frame(parent, bd=1, relief="solid", padx=5, pady=5)

    tk.Label(frame, text="Publisher Name : ").grid(row=0, column=0, sticky="w")
    topic_entry = tk.Entry(frame)
    topic_entry.grid(row=0, column=1, sticky="ew", padx=2)
    start_button = tk.Button(frame, text="Start", command=handle_start)
    start_button.grid(row=0, column=2, sticky="e", padx=2)

    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
    text_area.insert(tk.END, "")
    text_area.configure(state="disabled")
    text_area.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5)

    message_entry = tk.Entry(frame, state="disabled")
    message_entry.bind("<Return>", lambda event: send_message())
    message_entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2)
    send_button = tk.Button(
        frame, text="Send", command=send_message, state="disabled")
    send_button.grid(row=2, column=2, sticky="e", padx=2)

    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    return frame
