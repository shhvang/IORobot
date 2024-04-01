from IO import kiyo

async def send_boot_message():
    support_chat_id = -1002146661683  # Support Chat ID
    boot_message = "Booting was succesfull!/nKiyo is alive again"
    await kiyo.client.send_message(support_chat_id, boot_message)

if __name__ == "__main__":
    kiyo.run()
    send_boot_message()