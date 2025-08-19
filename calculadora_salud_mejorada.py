#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 11:14:16 2025

@author: miguelsevillano
"""

import streamlit as st

# 🧠 Funciones de cálculo
def calcular_IMC(peso: float, altura: float) -> float:
    if altura <= 0:
        raise ValueError("La altura debe ser mayor que cero.")
    return peso / (altura ** 2)

def calcular_porcentaje_grasa(peso: float, altura: float, edad: int, valor_genero: float) -> float:
    imc = calcular_IMC(peso, altura)
    return 1.2 * imc + 0.23 * edad - 5.4 - valor_genero

def calcular_calorias_en_reposo(peso: float, altura: float, edad: int, valor_genero: float) -> float:
    return 10 * peso + 6.25 * altura - 5 * edad + valor_genero

def calcular_calorias_en_actividad(peso: float, altura: float, edad: int, valor_genero: float, valor_actividad: float) -> float:
    tmb = calcular_calorias_en_reposo(peso, altura, edad, valor_genero)
    return tmb * valor_actividad

def consumo_calorias_recomendada_para_adelgazar(tmb: float) -> tuple:
    return tmb * 0.80, tmb * 0.85

def clasificar_imc(imc: float) -> tuple:
    if imc < 18.5:
        return "🔸 Bajo peso", "orange", [
            "Aguacate", "Frutos secos", "Batidos con avena y leche entera", "Pan integral con mantequilla de maní"
        ]
    elif imc < 25:
        return "✅ Peso normal", "green", [
            "Verduras frescas", "Frutas variadas", "Proteínas magras (pollo, pescado)", "Granos integrales"
        ]
    elif imc < 30:
        return "⚠️ Sobrepeso", "yellow", [
            "Ensaladas con legumbres", "Frutas con bajo índice glucémico", "Carnes magras", "Agua en lugar de bebidas azucaradas"
        ]
    else:
        return "🚨 Obesidad", "red", [
            "Verduras al vapor", "Proteínas vegetales (tofu, lentejas)", "Frutas con fibra", "Evitar fritos y harinas refinadas"
        ]

# 🎨 Interfaz Streamlit
st.set_page_config(page_title="Calculadora de Salud Corporal", page_icon="🧬")
st.title("🧬 Calculadora Integral de Salud Corporal")

# 📥 Entradas del usuario
peso = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, value=70.0)
altura_m = st.number_input("Altura (m):", min_value=1.0, max_value=2.5, value=1.65)
altura_cm = altura_m * 100
edad = st.number_input("Edad:", min_value=10, max_value=100, value=32)
sexo = st.selectbox("Sexo:", ["Hombre", "Mujer"])
actividad = st.selectbox("Nivel de actividad física:", [
    "Sedentario (poco o ningún ejercicio)",
    "Ligero (1-3 días/semana)",
    "Moderado (3-5 días/semana)",
    "Intenso (6-7 días/semana)",
    "Muy intenso (dos veces al día)"
])

# 🔢 Valores según sexo y actividad
valor_genero = 5 if sexo == "Hombre" else -161
valor_grasa = 10.8 if sexo == "Hombre" else 0
actividad_dict = {
    "Sedentario (poco o ningún ejercicio)": 1.2,
    "Ligero (1-3 días/semana)": 1.375,
    "Moderado (3-5 días/semana)": 1.55,
    "Intenso (6-7 días/semana)": 1.725,
    "Muy intenso (dos veces al día)": 1.9
}
valor_actividad = actividad_dict[actividad]

# 🧮 Botón para calcular
if st.button("Calcular"):
    try:
        imc = calcular_IMC(peso, altura_m)
        clasificacion, color, alimentos = clasificar_imc(imc)
        grasa = calcular_porcentaje_grasa(peso, altura_m, edad, valor_grasa)
        tmb = calcular_calorias_en_reposo(peso, altura_cm, edad, valor_genero)
        tmb_actividad = calcular_calorias_en_actividad(peso, altura_cm, edad, valor_genero, valor_actividad)
        calorias_min, calorias_max = consumo_calorias_recomendada_para_adelgazar(tmb)

        st.subheader("📊 Resultados")
        st.markdown(f"<span style='color:{color}; font-size:20px;'>IMC: {imc:.2f} → {clasificacion}</span>", unsafe_allow_html=True)
        st.write(f"✅ % Grasa Corporal: {grasa:.2f}%")
        st.write(f"🔥 TMB en reposo: {tmb:.2f} kcal/día")
        st.write(f"🔥 TMB ajustada por actividad: {tmb_actividad:.2f} kcal/día")
        st.success(f"🥦 Para adelgazar se recomienda consumir entre {calorias_min:.2f} y {calorias_max:.2f} kcal/día")

        st.subheader("🍽️ Recomendaciones Alimenticias")
        st.markdown("Según tu IMC, te recomendamos incluir en tu dieta:")
        for alimento in alimentos:
            st.markdown(f"- {alimento}")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
