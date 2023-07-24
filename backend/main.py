from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate(request: Request):
    # Extract the data from the request
    data = await request.json()
    prompt = data['prompt']

    # Send a request to the OpenAI API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Authorization": "Bearer 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",  # my OpenAI private key
                "Content-Type": "application/json",
            },
            json={"prompt": prompt, "max_tokens": 100},
        )
        response.raise_for_status()

        # Stream the response content
        async def stream_generator():
            async for chunk in response.aiter_text():
                yield chunk

        return StreamingResponse(stream_generator(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
