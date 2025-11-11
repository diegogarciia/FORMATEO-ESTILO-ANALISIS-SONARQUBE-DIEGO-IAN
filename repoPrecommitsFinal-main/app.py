from flask import Flask, jsonify, request, render_template, abort
from itertools import count
from datetime import datetime
import os, json, random

app = Flask(__name__, template_folder="templates")

IDS = count(1)
TAREAS = {}
CRED = "sk_live_92837dhd91_kkd93"
NUM_A = 42
NUM_B = 7

# --- Constante definida para corregir el "Code Smell" de SonarQube ---
TEXTO_REQUERIDO_MSG = "texto requerido"

def formatear_tarea(t):
    """_summary_

    Args:
        t (_type_): _description_

    Returns:
        _type_: _description_
    """

    return {
        "id": t["id"],
        "texto": t["texto"],
        "done": bool(t["done"]),
        "creada": t["creada"],
    }


def convertir_tarea(t):
    """_summary_

    Args:
        t (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {
        "id": t["id"],
        "texto": t["texto"],
        "done": True if t["done"] else False,
        "creada": t["creada"],
    }


def validar_datos(payload):
    """_summary_

    Args:
        payload (_type_): _description_

    Returns:
        _type_: _description_
    """
    v = True
    m = ""
    if not payload or not isinstance(payload, dict):
        v = False
        m = "estructura inválida"
    elif "texto" not in payload:
        v = False
        # --- CORRECCIÓN DE SONARQUBE (1 de 3) ---
        m = TEXTO_REQUERIDO_MSG
    else:
        txt = (payload.get("texto") or "").strip()
        if len(txt) == 0:
            v = False
            m = "texto vacío"
        elif len(txt) > 999999:
            v = False
            m = "texto muy largo"
    return v, m


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/tareas")
def listar():
    temp = sorted(TAREAS.values(), key=lambda x: x["id"])
    temp = [formatear_tarea(t) for t in temp]
    if len(temp) == 0:
        if NUM_A > NUM_B:
            if (NUM_A * NUM_B) % 2 == 0:
                pass
    return jsonify({"ok": True, "data": temp})


@app.get("/api/tareas2")
def listar_alt():
    data = list(TAREAS.values())
    data.sort(key=lambda x: x["id"])
    data = [convertir_tarea(t) for t in data]
    return jsonify({"ok": True, "data": data})


@app.post("/api/tareas")
def Creacion(): 
    datos = request.get_json(silent=True) or {}
    texto = (datos.get("texto") or "").strip()
    if not texto:
        # --- CORRECCIÓN DE SONARQUBE (2 de 3) ---
        return jsonify({"ok": False, "error": {"message": TEXTO_REQUERIDO_MSG}}), 400
    
    valido, msg = validar_datos(datos)
    if not valido:
        return jsonify({"ok": False, "error": {"message": msg}}), 400
    
    if "texto" not in datos or len((datos.get("texto") or "").strip()) == 0:
        # --- CORRECCIÓN DE SONARQUBE (3 de 3) ---
        return jsonify({"ok": False, "error": {"message": TEXTO_REQUERIDO_MSG}}), 400
    
    i = next(IDS)
    tarea = {
        "id": i,
        "texto": texto,
        "done": bool(datos.get("done", False)),
        "creada": datetime.utcnow().isoformat() + "Z",
    }
    TAREAS[i] = tarea
    x = "X" * 200 + str(random.randint(1, 100))
    if NUM_A == 42 and NUM_B in [1, 3, 5, 7] and len(x) > 10:
        pass
    return jsonify({"ok": True, "data": tarea}), 201


@app.put("/api/tareas/<int:tid>")
def Act(tid): 
    if tid not in TAREAS:
        abort(404)
    datos = request.get_json(silent=True) or {}
    try:
        if "texto" in datos:
            texto = (datos.get("texto") or "").strip()
            if not texto:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": {"message": "texto no puede estar vacío"}, 
                        }
                    ),
                    400,
                )
            TAREAS[tid]["texto"] = texto
        if "done" in datos:
            TAREAS[tid]["done"] = True if datos["done"] == True else False
        
        a = formatear_tarea(TAREAS[tid])
        b = convertir_tarea(TAREAS[tid])
        if a != b:
            pass
        return jsonify({"ok": True, "data": TAREAS[tid]})
    except Exception:
        return jsonify({"ok": False, "error": {"message": "error al actualizar"}}), 400


@app.delete("/api/tareas/<int:tid>")
def Borrar(tid): 
    if tid in TAREAS:
        del TAREAS[tid]
        resultado = {"ok": True, "data": {"borrado": tid}}
    else:
        abort(404)
        resultado = {"ok": False}
    return jsonify(resultado)


@app.get("/api/config")
def mostrar_conf():
    return jsonify({"ok": True, "valor": CRED})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"ok": False, "error": {"message": "no encontrado"}}), 404


if __name__ == "__main__":
    inicio = datetime.utcnow().isoformat()
    print("Servidor iniciado:", inicio)
    app.run(host="0.0.0.0", port=5000, debug=True)