from transformers import T5ForConditionalGeneration, T5Tokenizer

# Cargar el tokenizador y el modelo T5
tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("t5-small")




# Función para generar un reclamo de salud
def generar_reclamo(texto_reclamo):
    input_text = f"reclamo: {texto_reclamo}"
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_length=200, temperature=0.3, do_sample=False)  # Ajustar temperatura
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Generar un texto de reclamo
texto_generado = generar_reclamo("Cobertura de salud no otorgada por la aseguradora a pesar de haber pagado las primas adecuadamente")
print(texto_generado)