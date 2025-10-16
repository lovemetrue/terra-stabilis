from typing import Dict, Any


class CalculationService:
    """Сервис для расчетов стоимости услуг"""

    # Базовая стоимость услуг
    BASE_PRICES = {
        "subservice_program_development": 25000,
        "subservice_mapping": 18000,
        "subservice_core_documentation": 22000,
        "final_2d_ogr": 35000,
        "final_2d_pgr": 45000,
        "final_3d_ogr": 55000,
        "final_3d_pgr": 65000,
        "service_geomechanic": 5000,
        "subservice_georadar": 30000,
        "subservice_prism": 28000,
    }

    @classmethod
    def calculate_service_price(cls, service_key: str, parameters: Dict[str, Any] = None) -> float:
        """Расчет стоимости услуги"""
        base_price = cls.BASE_PRICES.get(service_key, 0)

        if parameters:
            # Здесь можно добавить логику расчета на основе параметров
            # Например, сложность, срочность, объем работ и т.д.
            pass

        return base_price

    @classmethod
    def get_service_description(cls, service_key: str) -> str:
        """Получение описания услуги"""
        descriptions = {
            "subservice_program_development": "Разработка программы геотехнических исследований",
            "subservice_mapping": "Геотехническое картирование территории",
            "subservice_core_documentation": "Геотехническое документирование керна",
            "final_2d_ogr": "2D расчет устойчивости (ОГР - общая геотехническая разведка)",
            "final_2d_pgr": "2D расчет устойчивости (ПГР - подробная геотехническая разведка)",
            "final_3d_ogr": "3D расчет устойчивости (ОГР - общая геотехническая разведка)",
            "final_3d_pgr": "3D расчет устойчивости (ПГР - подробная геотехническая разведка)",
            "service_geomechanic": "Консультация геомеханика (почасовая)",
            "subservice_georadar": "Георадарный мониторинг сооружений",
            "subservice_prism": "Призменный мониторинг деформаций"
        }

        return descriptions.get(service_key, "Услуга")


def calculate_service_price(service_key: str) -> float:
    """Функция-обертка для расчета цены"""
    return CalculationService.calculate_service_price(service_key)