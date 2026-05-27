# Presentación Streamlit — Mercado 2 Starbucks América

Presentación tipo slides para el Trabajo 2 de AEM 2026-1.

## Cómo correrla

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Lanzar la app

```bash
streamlit run app.py
```

Se abre en `http://localhost:8501`. Usa la sidebar izquierda para navegar entre slides, o las flechas inferiores.

## Estructura de la presentación

12 slides + portada:

1. **Portada** — Título y autores
2. **Contexto del mercado** — Cliente, pregunta de negocio
3. **El dataset** — Variables disponibles
4. **Limpieza y preparación** — Transformaciones
5. **Metodología** — 4 modelos en paralelo
6. **Modelo RFM** — K-Means K=3
7. **Modelo Sociodemográfico** — LCA K=3
8. **Comparación formal** — Elección de método por dimensión
9. **Matriz cruzada** — 9 segmentos finales
10. **Afinidades** — Caracterización por experiencia
11. **Mercados meta** — Criterios STP
12. **Posicionamiento** — Propuesta de valor por segmento
13. **Conclusiones** — Hallazgos, limitaciones, próximos pasos

## Notas

- Los datos están **hardcoded** desde los outputs reales del notebook, así que la app corre **sin necesidad** de tener `s_order.csv` ni de re-ejecutar el modelo.
- Si quieren conectarla al notebook (para que tome datos del CSV exportado en `outputs/`), pueden modificar la sección "DATOS" en `app.py` para leer los CSVs en lugar de los DataFrames inline.
- La paleta está alineada con la identidad Starbucks: verde oscuro `#006241`, dorado `#cba258`, rojo de acento `#d62828`.
- Funciona bien en pantalla de proyección (layout `wide`, sidebar plegable).

## Antes de presentar

- [ ] Revisar la slide 6 (Modelo Sociodemográfico): los nombres "Perfil Nicho A", "Mainstream Mayoritario", "Perfil Nicho B" son **placeholders**. Reemplázenlos por los nombres reales que surjan del bloque "Parte 2.5 — Caracterización" del notebook.
- [ ] Si los nombres cambian, hay que actualizarlos en:
  - El diccionario `NOMBRES_SOCIO` del notebook
  - Las constantes `SOCIO_PROFILE`, `MATRIZ`, `AFINIDAD` en `app.py`
- [ ] Probar la navegación con teclado en modo pantalla completa de Streamlit.
