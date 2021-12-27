from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple, ClassVar, TypeVar, Type


@dataclass(frozen=True)
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информацию о тренировке."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

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
            f'Определите get_spent_calories в {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )

T = TypeVar("T", bound=Training)


class Running(Training):
    """Тренировка: бег."""

    RATE_CALORIE_RUN_LEFT: float = 18
    RATE_CALORIE_RUN_RIGHT: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        first_part: float = (
            self.RATE_CALORIE_RUN_LEFT
            * self.get_mean_speed() - self.RATE_CALORIE_RUN_RIGHT
        )
        spent_calories: float = (
            first_part
            * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATE_CALORIE_WALK_LEFT: float = 0.035
    RATE_CALORIE_WALK_RIGHT: float = 0.029

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

        spent_calories: float = (
            self.get_mean_speed() ** 2 // self.height
            * self.RATE_CALORIE_WALK_RIGHT * self.weight
            + self.RATE_CALORIE_WALK_LEFT * self.weight
            * self.duration * self.MINUTES_IN_HOUR
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    RATE_CALORIE_SWIM_LEFT: float = 1.1
    RATE_CALORIE_SWIM_RIGHT: float = 2

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

        return (
            (self.get_mean_speed() + self.RATE_CALORIE_SWIM_LEFT)
            * self.RATE_CALORIE_SWIM_RIGHT * self.weight
        )

    def get_mean_speed(self) -> float:
        """Получить дистанцию в км."""

        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dictionary: Dict[str, Type[T]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    try:
        return dictionary[workout_type](*data)
    except KeyError as error:
        print(
            f'KeyError: не удалось получить значение по ключу: '
            f'{error}'
        )
        raise ValueError


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
