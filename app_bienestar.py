"""App de bienestar personal: meditación, rutina y journal.

Incluye un flujo EJE inspirado en UX minimalista:
- Prueba gratuita de 7 días.
- Pregunta emocional para personalizar primera sesión.
- Primera sesión inmediata orientada a foco.

Los datos se guardan en JSON para mantener un historial simple.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import time
from typing import Any


DATE_FORMAT = "%Y-%m-%d"
AMBIENTES = {
    "foco": ["lluvia suave", "ruido marrón", "piano ambiental"],
    "relax": ["océano profundo", "viento nocturno", "bosque"],
    "sueño": ["ruido rosa", "lluvia nocturna", "drone cálido"],
}

AUDIOS_ENFOQUE = [
    {"nombre": "focus stream (youtube)", "url": "https://www.youtube.com/watch?v=ilXtdnLsZVg"},
    {"nombre": "deep focus binaural", "url": "https://www.youtube.com/results?search_query=deep+focus+binaural"},
    {"nombre": "minimal lo-fi focus", "url": "https://www.youtube.com/results?search_query=minimal+lofi+focus"},
]

ESTADOS_MENTALES = ["saturada", "ansiosa", "dispersa", "cansada", "clara pero tensa"]

SESION_POR_ESTADO = {
    "saturada": {"titulo": "Reset Inicial", "subtitulo": "Reducir interferencia básica.", "minutos": 3},
    "ansiosa": {"titulo": "Aterrizar", "subtitulo": "Bajar activación y recuperar eje.", "minutos": 3},
    "dispersa": {"titulo": "Foco Núcleo", "subtitulo": "Recuperar dirección en un solo punto.", "minutos": 3},
    "cansada": {"titulo": "Recarga Suave", "subtitulo": "Ordenar mente con baja exigencia.", "minutos": 3},
    "clara pero tensa": {"titulo": "Precisión Calma", "subtitulo": "Sostener claridad sin presión corporal.", "minutos": 3},
}


@dataclass
class Meditacion:
    fecha: str
    minutos: int
    tecnica: str


@dataclass
class TareaRutina:
    nombre: str
    completada: bool = False


@dataclass
class EntradaJournal:
    fecha: str
    titulo: str
    contenido: str
    estado_animo: str


class AppBienestar:
    def __init__(self, data_file: str = "bienestar_data.json") -> None:
        self.data_path = Path(data_file)
        self.data = self._load_data()

    def _load_data(self) -> dict[str, Any]:
        if not self.data_path.exists():
            return {
                "meditaciones": [],
                "rutinas": [],
                "journal": [],
                "sesiones_foco": [],
                "onboarding": {},
            }

        with self.data_path.open("r", encoding="utf-8") as file:
            payload: dict[str, Any] = json.load(file)

        payload.setdefault("meditaciones", [])
        payload.setdefault("rutinas", [])
        payload.setdefault("journal", [])
        payload.setdefault("sesiones_foco", [])
        payload.setdefault("onboarding", {})
        return payload

    def _save_data(self) -> None:
        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def _today() -> str:
        return datetime.now().strftime(DATE_FORMAT)

    def resumen_prueba_gratuita(self) -> dict[str, str | int]:
        return {
            "dias_gratis": 7,
            "precio_mensual_usd": 7,
            "mensaje": "7 días gratis. Luego USD 7/mes. Cancelás cuando quieras.",
        }

    def obtener_estados_mentales(self) -> list[str]:
        return ESTADOS_MENTALES.copy()

    def crear_primera_sesion(self, estado_mental: str) -> dict[str, Any]:
        estado = estado_mental.strip().lower()
        if estado not in SESION_POR_ESTADO:
            raise ValueError("Estado mental no soportado.")

        plan = SESION_POR_ESTADO[estado].copy()
        plan["estado_mental"] = estado
        plan["objetivo"] = "foco"
        plan["voz"] = "femenina"
        return plan

    def guardar_onboarding(self, email: str, estado_mental: str, tono: str = "híbrido") -> None:
        self.data["onboarding"] = {
            "email": email.strip().lower(),
            "estado_mental": estado_mental.strip().lower(),
            "tono": tono,
            "fecha": self._today(),
        }
        self._save_data()

    def registrar_meditacion(self, minutos: int, tecnica: str, fecha: str | None = None) -> Meditacion:
        if minutos <= 0:
            raise ValueError("Los minutos deben ser mayores a 0.")

        registro = Meditacion(fecha=fecha or self._today(), minutos=minutos, tecnica=tecnica.strip())
        self.data["meditaciones"].append(asdict(registro))
        self._save_data()
        return registro

    def agregar_tarea_rutina(self, nombre: str) -> TareaRutina:
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("La tarea no puede estar vacía.")

        tarea = TareaRutina(nombre=nombre_limpio)
        self.data["rutinas"].append(asdict(tarea))
        self._save_data()
        return tarea

    def completar_tarea(self, nombre: str) -> bool:
        objetivo = nombre.strip().lower()
        for tarea in self.data["rutinas"]:
            if tarea["nombre"].lower() == objetivo:
                tarea["completada"] = True
                self._save_data()
                return True
        return False

    def escribir_journal(self, titulo: str, contenido: str, estado_animo: str, fecha: str | None = None) -> EntradaJournal:
        if not titulo.strip() or not contenido.strip():
            raise ValueError("Título y contenido son obligatorios.")

        entrada = EntradaJournal(
            fecha=fecha or self._today(),
            titulo=titulo.strip(),
            contenido=contenido.strip(),
            estado_animo=estado_animo.strip() or "neutral",
        )
        self.data["journal"].append(asdict(entrada))
        self._save_data()
        return entrada

    def recomendar_ambiente(self, objetivo: str) -> list[str]:
        return AMBIENTES.get(objetivo.lower(), ["lluvia suave", "bosque"])

    def obtener_audios_enfoque(self) -> list[dict[str, str]]:
        return [audio.copy() for audio in AUDIOS_ENFOQUE]

    def registrar_sesion_foco(
        self,
        minutos: int,
        objetivo: str,
        ambiente: str,
        audio_enfoque: dict[str, str],
        fecha: str | None = None,
    ) -> dict[str, Any]:
        if minutos <= 0:
            raise ValueError("La sesión debe durar al menos 1 minuto.")

        sesion = {
            "fecha": fecha or self._today(),
            "minutos": minutos,
            "objetivo": objetivo.strip().lower() or "foco",
            "ambiente": ambiente.strip().lower() or "lluvia suave",
            "audio_enfoque": audio_enfoque.get("nombre", "").strip().lower() or AUDIOS_ENFOQUE[0]["nombre"],
            "audio_url": audio_enfoque.get("url", "").strip() or AUDIOS_ENFOQUE[0]["url"],
        }
        self.data["sesiones_foco"].append(sesion)
        self._save_data()
        return sesion

    def resumen_diario(self, fecha: str | None = None) -> dict[str, Any]:
        fecha_objetivo = fecha or self._today()
        meditaciones = [m for m in self.data["meditaciones"] if m["fecha"] == fecha_objetivo]
        journal_entries = [j for j in self.data["journal"] if j["fecha"] == fecha_objetivo]
        sesiones_foco = [s for s in self.data["sesiones_foco"] if s["fecha"] == fecha_objetivo]
        tareas_total = len(self.data["rutinas"])
        tareas_completadas = sum(1 for t in self.data["rutinas"] if t["completada"])

        return {
            "fecha": fecha_objetivo,
            "minutos_meditados": sum(m["minutos"] for m in meditaciones),
            "sesiones_meditacion": len(meditaciones),
            "minutos_foco": sum(s["minutos"] for s in sesiones_foco),
            "sesiones_foco": len(sesiones_foco),
            "tareas_completadas": tareas_completadas,
            "tareas_totales": tareas_total,
            "entradas_journal": len(journal_entries),
        }


def ejecutar_sesion_guiada(minutos: int, ambiente: str, audio_enfoque: dict[str, str]) -> None:
    bloques = min(4, max(1, minutos))
    mensajes = [
        "Respira profundo...",
        "Suelta tensión de hombros y mandíbula...",
        "Vuelve al presente con calma...",
        "Mantén una atención suave y estable...",
    ]

    print(f"\n🎧 Ambiente seleccionado: {ambiente}")
    print(f"🎶 Audio de enfoque: {audio_enfoque['nombre']}")
    print(f"🔗 Link: {audio_enfoque['url']}")
    print("Iniciando sesión estilo Endel (simulada)...")
    for i in range(bloques):
        print(f"[{i + 1}/{bloques}] {mensajes[i]}")
        time.sleep(1)
    print("✅ Sesión finalizada. Buen trabajo.\n")


def ejecutar_flow_eje(app: AppBienestar) -> None:
    prueba = app.resumen_prueba_gratuita()
    print("\n🖤 EJE · precisión, silencio, control")
    print("Comenzar prueba gratuita")
    print(f"{prueba['dias_gratis']} días gratis. Luego USD {prueba['precio_mensual_usd']}/mes.")

    print("\nCreá tu acceso.")
    email = input("Email: ").strip()
    _password = input("Contraseña: ").strip()
    print("No enviamos spam. Solo acceso a tu entrenamiento.")

    print("\n¿Cómo está tu mente hoy?")
    estados = app.obtener_estados_mentales()
    for i, estado in enumerate(estados, start=1):
        print(f"{i}) {estado.capitalize()}")
    seleccion = input("Elegí una opción: ").strip() or "1"
    try:
        estado = estados[int(seleccion) - 1]
    except (ValueError, IndexError):
        estado = estados[0]

    print("\nActivá tu prueba gratuita.")
    print(prueba["mensaje"])
    _tarjeta = input("Tarjeta (simulada): ").strip()
    print("Te avisamos antes de que termine tu prueba.")

    app.guardar_onboarding(email, estado, tono="híbrido")
    plan = app.crear_primera_sesion(estado)

    print("\nBienvenida a EJE.")
    print("Tu mente ya empezó a bajar la interferencia.")
    input("Enter para comenzar primera sesión...")

    audios = app.obtener_audios_enfoque()
    ambiente = app.recomendar_ambiente("foco")[0]
    audio_enfoque = audios[0]
    app.registrar_sesion_foco(plan["minutos"], plan["objetivo"], ambiente, audio_enfoque)

    print(f"\n🎧 {plan['titulo']}")
    print(plan["subtitulo"])
    print("Voz: femenina")
    ejecutar_sesion_guiada(plan["minutos"], ambiente, audio_enfoque)


def ejecutar_app() -> None:
    app = AppBienestar()

    menu = """
=== App de Bienestar ===
1) Registrar meditación
2) Agregar tarea de rutina
3) Completar tarea
4) Escribir en journal
5) Ver resumen de hoy
6) Iniciar sesión foco/relax (estilo Endel)
7) Flow EJE (prueba gratis + primera sesión)
8) Salir
"""

    while True:
        print(menu)
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            minutos = int(input("Minutos de meditación: "))
            tecnica = input("Técnica (respiración, guiada, etc.): ")
            registro = app.registrar_meditacion(minutos, tecnica)
            print(f"✅ Meditación registrada: {registro}")

        elif opcion == "2":
            nombre = input("Nombre de la tarea: ")
            tarea = app.agregar_tarea_rutina(nombre)
            print(f"✅ Tarea agregada: {tarea.nombre}")

        elif opcion == "3":
            nombre = input("Nombre de la tarea a completar: ")
            if app.completar_tarea(nombre):
                print("✅ Tarea completada.")
            else:
                print("⚠️ No encontré una tarea con ese nombre.")

        elif opcion == "4":
            titulo = input("Título: ")
            contenido = input("¿Qué quieres escribir hoy?: ")
            estado_animo = input("Estado de ánimo: ")
            entrada = app.escribir_journal(titulo, contenido, estado_animo)
            print(f"✅ Entrada guardada: {entrada.titulo}")

        elif opcion == "5":
            resumen = app.resumen_diario()
            print("\n📊 Resumen de hoy")
            for clave, valor in resumen.items():
                print(f"- {clave}: {valor}")

        elif opcion == "6":
            objetivo = input("Objetivo (foco/relax/sueño): ").strip().lower() or "foco"
            sugerencias = app.recomendar_ambiente(objetivo)
            audios = app.obtener_audios_enfoque()
            print("\nAmbientes sugeridos:")
            for idx, amb in enumerate(sugerencias, start=1):
                print(f"{idx}) {amb}")

            seleccion = input("Elige un número de ambiente (Enter = 1): ").strip() or "1"
            try:
                ambiente = sugerencias[int(seleccion) - 1]
            except (ValueError, IndexError):
                ambiente = sugerencias[0]

            print("\nAudios de enfoque:")
            for idx, audio in enumerate(audios, start=1):
                print(f"{idx}) {audio['nombre']} -> {audio['url']}")

            seleccion_audio = input("Elige un audio de enfoque (Enter = 1): ").strip() or "1"
            try:
                audio_enfoque = audios[int(seleccion_audio) - 1]
            except (ValueError, IndexError):
                audio_enfoque = audios[0]

            minutos = int(input("Duración de sesión (minutos): "))
            app.registrar_sesion_foco(minutos, objetivo, ambiente, audio_enfoque)
            ejecutar_sesion_guiada(minutos, ambiente, audio_enfoque)

        elif opcion == "7":
            ejecutar_flow_eje(app)

        elif opcion == "8":
            print("¡Hasta pronto! 🌿")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    ejecutar_app()
