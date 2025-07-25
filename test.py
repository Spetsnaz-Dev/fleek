import os
import replicate
from replicate.exceptions import ModelError
print(os.getenv("REPLICATE_API_TOKEN"))
try:
  output = replicate.Client(api_token="r8_YourActualTokenHere").run(
    "stability-ai/stable-diffusion",
    input={"prompt": "An astronaut riding a rainbow unicorn"}
)
  print(output)
except ModelError as e:
  if "(some known issue)" in e.prediction.logs:
    pass

  print("Failed prediction: " + e.prediction.id)