"""------------------------------------------------------
D10Z – Módulo Neuro
Integración oficial con MorphoPy para análisis morfológico neuronal.

Este módulo permite:
- Cargar morfologías neuronales (.swc)
- Calcular estadísticas morfométricas
- Calcular diagramas de persistencia TDA
- Generar mapas de densidad
- Usar MorphoPy como backend dentro del marco D10Z

Autor: Jamil Al Thani
"""

import os
import morphopy as mp
from morphopy import morphology as mp_morph
from morphopy import features as mp_features
from morphopy import density as mp_density
from morphopy import persistence as mp_persist


class Neuro:
    """
    Interfaz unificada para acceso neuronal dentro del ecosistema D10Z.
    """

    def __init__(self, swc_path: str):
        if not os.path.exists(swc_path):
            raise FileNotFoundError(f"Archivo SWC no encontrado: {swc_path}")

        self.swc_path = swc_path
        self.neuron = mp_morph.Neuron(swc_path)

    # ----------------------------------------------------------------------
    # Estadísticas Morfométricas
    # ----------------------------------------------------------------------
    def stats(self) -> dict:
        """
        Retorna 28 estadísticas morfométricas estándar.
        """
        return mp_features.compute_stats(self.neuron)

    # ----------------------------------------------------------------------
    # Diagramas de Persistencia (Topología)
    # ----------------------------------------------------------------------
    def persistence(self, mode: str = "radial_distance"):
        """
        Calcula el diagrama de persistencia.
        """
        return mp_persist.get_persistence(self.neuron, func=mode)

    # ----------------------------------------------------------------------
    # Mapas de Densidad
    # ----------------------------------------------------------------------
    def density_maps(self, config_file: str = None):
        """
        Genera mapas de densidad neuronal.
        """
        return mp_density.compute_density_maps(
            self.neuron, config_file=config_file
        )

    # ----------------------------------------------------------------------
    # Información del Soma / Estructura
    # ----------------------------------------------------------------------
    def summary(self) -> dict:
        """
        Resumen estructural general.
        """
        return {
            "total_nodes": len(self.neuron.nodes),
            "total_edges": len(self.neuron.edges),
            "soma_position": self.neuron.soma,
            "bounding_box": self.neuron.bounding_box,
        }

    # ----------------------------------------------------------------------
    # Exportación de datos
    # ----------------------------------------------------------------------
    def export_density(self, outdir: str):
        """
        Guarda mapas de densidad como imágenes.
        """
        os.makedirs(outdir, exist_ok=True)
        dm = mp_density.compute_density_maps(self.neuron)
        for k, v in dm.items():
            fig = v["figure"]
            fig.savefig(os.path.join(outdir, f"density_{k}.png"))


__all__ = ["Neuro"]
