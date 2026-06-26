import serial
import anthropic

PORT = "/dev/tty.usbmodem1102"  # adjust to your board's serial port
BAUD = 115200

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
ser = serial.Serial(PORT, BAUD, timeout=1)

while True:
    line = ser.readline().decode("utf-8").strip()
    if not line.startswith("TEMP:"):
        continue

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=20,
        messages=[{
            "role": "user",
            "content": f"In 4 words or fewer, describe this room's mood: {line}",
        }],
    )

    reply = response.content[0].text.strip()
    print("LLM:", reply)
    ser.write((reply + "\n").encode("utf-8"))
