import tempfile
import unittest
from pathlib import Path

from app_bienestar import AppBienestar


class TestAppBienestar(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "data.json"
        self.app = AppBienestar(str(self.db_path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_registrar_meditacion(self):
        registro = self.app.registrar_meditacion(15, "respiración", fecha="2026-01-01")
        self.assertEqual(registro.minutos, 15)
        self.assertEqual(self.app.resumen_diario("2026-01-01")["minutos_meditados"], 15)

    def test_completar_tarea(self):
        self.app.agregar_tarea_rutina("Tomar agua")
        resultado = self.app.completar_tarea("Tomar agua")
        self.assertTrue(resultado)
        resumen = self.app.resumen_diario("2026-01-01")
        self.assertEqual(resumen["tareas_completadas"], 1)

    def test_escribir_journal(self):
        entrada = self.app.escribir_journal(
            "Día productivo",
            "Terminé mis pendientes y medité 10 minutos.",
            "agradecido",
            fecha="2026-01-01",
        )
        self.assertEqual(entrada.estado_animo, "agradecido")
        self.assertEqual(self.app.resumen_diario("2026-01-01")["entradas_journal"], 1)

    def test_sesion_foco_y_recomendaciones(self):
        sugerencias = self.app.recomendar_ambiente("foco")
        audios = self.app.obtener_audios_enfoque()
        self.assertGreaterEqual(len(sugerencias), 1)
        self.assertGreaterEqual(len(audios), 1)
        self.assertIn("lluvia suave", sugerencias)
        self.assertEqual(audios[0]["url"], "https://www.youtube.com/watch?v=ilXtdnLsZVg")

        sesion = self.app.registrar_sesion_foco(20, "foco", sugerencias[0], audios[0], fecha="2026-01-01")
        self.assertEqual(sesion["minutos"], 20)
        self.assertEqual(sesion["audio_enfoque"], audios[0]["nombre"])
        self.assertEqual(sesion["audio_url"], audios[0]["url"])
        resumen = self.app.resumen_diario("2026-01-01")
        self.assertEqual(resumen["minutos_foco"], 20)
        self.assertEqual(resumen["sesiones_foco"], 1)


if __name__ == "__main__":
    unittest.main()
