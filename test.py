import google.generativeai as genai

print([m.name for m in genai.list_models()])