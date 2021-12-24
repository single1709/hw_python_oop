from dataclasses import dataclass
from typing import Dict, List, Tuple, ClassVar


@dataclass(frozen=True)
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_INFORMATION: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информацию о тренировке."""

        return(self.TRAINING_INFORMATION.format(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""

    RATE_CALORIE_RUN1: float = 18
    RATE_CALORIE_RUN2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        first_part: float = ((self.RATE_CALORIE_RUN_1
                             * self.get_mean_speed() - self.RATE_CALORIE_RUN2))
        spent_calories: float = (first_part
                                 * self.weight / self.M_IN_KM
                                 * self.duration * self.MINUTES_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATE_CALORIE_WALK1: float = 0.035
    RATE_CALORIE_WALK2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        spent_calories: float = (self.get_mean_speed(self) ** 2 // self.height
                                 * self.RATE_CALORIE_WALK2 * self.weight
                                 + self.RATE_CALORIE_WALK1 * self.weight
                                 * self.duration * self.MINUTES_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    RATE_CALORIE_SWIM1: float = 1.1
    RATE_CALORIE_SWIM2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        """Получить дистанцию в км."""

        return ((self.get_mean_speed() + self.RATE_CALORIE_SWIM1)
                * self.RATE_CALORIE_SWIM2 * self.weight)

    def get_mean_speed(self) -> float:
        """Получить дистанцию в км."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dictionary: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if isinstance(data, list) and isinstance(workout_type, str):
        return dictionary[workout_type](*data)
    else:
        raise TypeError


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
