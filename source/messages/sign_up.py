__all__ = [
    "age_message",
    "location_message",
    "location_not_found_message",
    "photo_message",
    "photo_not_found_message",
    "sex_message",
    "start_message",
    "start_to_run_message",
]

start_message = (
    "Давай начнем наше знакомство, {name}! "
    "Чтобы найти подходящего собеседника, мне нужно знать твой возраст. "
    "Возраст принимается числом от 16 до 32 годиков:"
)
start_to_run_message = "Я уже успел заскучать.."

age_message = (
    "Так, с возрастом мы определились, а вот твой гендер остается в тайне:"
)
sex_message = "Осталось дело за малым, укажи свой город:"

photo_message = "Отлично получилось, а откуда ты?"
photo_not_found_message = "Давай посмотрим на тебя, скинь фоточку:"

location_message = "Успехов тебе! 😉"
location_not_found_message = "Город не удалось найти, попробуй снова.."
