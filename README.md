# images_service
GET /accounts - регистрация/логин/вход/загрузка и отображение изображений\n
GET /accounts/user - получение информации о текущем юзере
GET /accounts/image/<int:_id> - получение всех изображений пользователя у которого id=_id
POST /accounts/image/<int:_id> - загрузка фото для юзера с id=_id, есть параметр image - фото для загрузки
DELETE /accounts/image/<int:_id> - удаление фото с id=_id
POST /image/delete_all - удаление всех изображений из БД
