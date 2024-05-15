import asyncio
import websockets
import base64
import json

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            if 'type' in data:
                if data['type'] == 'text':
                    await websocket.send(json.dumps({'response': f"Received text: {data['message']}"}))
                elif data['type'] == 'json':
                    await websocket.send(json.dumps({'response': f"Received JSON: {data}"}))
                elif data['type'] == 'video':
                    video_data = base64.b64decode(data['data'])
                    await websocket.send(json.dumps({'response': 'Video received'}))
                elif data['type'] == 'pamonha':
                    await websocket.send(json.dumps({'response': 'Pamonha received'}))
        except json.JSONDecodeError:
            await websocket.send(json.dumps({'error': 'Invalid JSON'}))

start_server = websockets.serve(handler, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
