from typing import Union, Dict, List, Tuple


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """Возвращает информацию о тренировке."""

        return(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
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

        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        cf_1: int = 18
        cf_2: int = 20
        min: int = 60
        first_part: float = (cf_1 * self.get_mean_speed() - cf_2) * self.weight
        second_part: float = first_part / Training.M_IN_KM
        return second_part * (self.duration * min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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

        cfc_1: float = 0.035
        cfc_2: float = 0.029
        min: int = 60
        first_part_1: float = Training.get_mean_speed(self) ** 2 // self.height
        first_part_2: float = cfc_2 * self.weight
        first_part: float = first_part_1 * first_part_2
        second_part: float = cfc_1 * self.weight
        return first_part + second_part * self.duration * min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Получить дистанцию в км."""

        cf_1: float = 1.1
        cf_2: int = 2
        return (self.get_mean_speed() + cf_1) * cf_2 * self.weight

    def get_mean_speed(self) -> float:
        """Получить дистанцию в км."""
        first_part: float = self.length_pool * self.count_pool
        return first_part / Training.M_IN_KM / self.duration

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * Swimming.LEN_STEP / Swimming.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dictionary: Dict[str, Union[Swimming,
                                Running,
                                SportsWalking]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    return dictionary[workout_type](*data)


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
