import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Finanzas Personales", page_icon="💰", layout="centered")

st.title("📊 Aplicación de Finanzas Personales")

Base = declarative_base()
class Transaccion(Base):
    __tablename__ = 'transacciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)  # 'ingreso' o 'gasto'
    monto = Column(Float, nullable=False)
    descripcion = Column(String)

engine = create_engine('sqlite:///finanzas.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

with st.form("registro_transaccion"):
    st.subheader("Registrar Nueva Transacción")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    monto = st.number_input("Monto", min_value=0.0)
    descripcion = st.text_area("Descripción")
    submitted = st.form_submit_button("Guardar")

    if submitted:
        nueva_transaccion = Transaccion(
            tipo=tipo.lower(),
            monto=monto,
            descripcion=descripcion
        )
        session.add(nueva_transaccion)
        session.commit()
        st.success("Transacción registrada exitosamente!")

st.subheader("Historial de Transacciones")
transacciones = session.query(Transaccion).all()
if transacciones:
    datos = [
        {
            "ID": t.id,
            "Tipo": t.tipo,
            "Monto": t.monto,
            "Descripción": t.descripcion
        }
        for t in transacciones
    ]
    df = pd.DataFrame(datos)
    st.dataframe(df)

    st.subheader("Resumen Financiero")
    ingresos = sum(t.monto for t in transacciones if t.tipo == "ingreso")
    gastos = sum(t.monto for t in transacciones if t.tipo == "gasto")
    balance = ingresos - gastos

    st.write(f"**Total Ingresos:** ${ingresos}")
    st.write(f"**Total Gastos:** ${gastos}")
    st.write(f"**Balance:** ${balance}")
else:
    st.info("No hay transacciones registradas.")

session.close()
