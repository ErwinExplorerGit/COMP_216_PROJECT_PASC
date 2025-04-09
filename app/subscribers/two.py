import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import threading
from messages.alert import show_error

client = None

text_area = None
connect_button = None
topic_entries = []
client_id_entry = None
is_connected = False


def on_message(client, userdata, message):
    msg = f"Received from {message.topic}: {message.payload.decode()}\n"
    if text_area:
        text_area.configure(state="normal")
        text_area.insert(tk.END, msg)
        text_area.configure(state="disabled")
        text_area.see(tk.END)
    print(msg.strip())


def start_listening(client_id, topics):
    global client
    client = mqtt.Client(client_id=client_id,
                         callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect('localhost', 1883)
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    client.loop_start()


def stop_listening():
    global client
    if client:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker")


def set_ui_state(connected):
    if connected:
        client_id_entry.config(state="readonly")
        for entry in topic_entries:
            entry.config(state="readonly")
        connect_button.config(text="Stop")
    else:
        client_id_entry.config(state="normal")
        client_id_entry.delete(0, tk.END)

        text_area.configure(state="normal")
        text_area.delete("1.0", tk.END)
        text_area.configure(state="disabled")

        for entry in topic_entries:
            entry.config(state="normal")
            entry.delete(0, tk.END)

        connect_button.config(text="Connect")


def toggle_connection():
    global is_connected, connect_button, topic_entries, client_id_entry
    if not is_connected:
        client_id = client_id_entry.get().strip()
        if not client_id:
            show_error("Please enter a subscriber name.")
            return

        topics = [entry.get().strip()
                  for entry in topic_entries if entry.get().strip()]
        if not topics:
            show_error("Please enter at least one topic to subscribe to.")
            return

        start_listening(client_id, topics)
        set_ui_state(True)
        is_connected = True
    else:
        stop_listening()
        set_ui_state(False)
        is_connected = False


def create_subscriber_two(parent):
    global text_area, connect_button, topic_entries, client_id_entry

    frame = tk.Frame(parent, bd=1, relief="solid", padx=5, pady=5)

    tk.Label(frame, text="Subscriber Name : ").grid(
        row=0, column=0, sticky="w")
    client_id_entry = tk.Entry(frame)
    client_id_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
    text_area.insert(tk.END, "")
    text_area.configure(state="disabled")
    text_area.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)

    topic_entries.clear()
    for i in range(3):
        tk.Label(frame, text="Subscribe to :").grid(
            row=2+i, column=0, sticky="e", pady=2)
        entry = tk.Entry(frame)
        entry.grid(row=2+i, column=1, sticky="ew", pady=2)
        topic_entries.append(entry)

    connect_button = tk.Button(
        frame, text="Connect", command=toggle_connection)
    connect_button.grid(row=5, column=1, sticky="e", pady=5)

    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    return frame
