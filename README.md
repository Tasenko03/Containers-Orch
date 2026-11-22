# Containers & Orchestration

Командный репозиторий для лабораторных по курсу «Контейнеризация и оркестрация».

## Команда

- [@Tasenko03](https://github.com/Tasenko03)
- [@RuslanAbliazov](https://github.com/RuslanAbliazov)
- [@Sckolver](https://github.com/Sckolver)

## Лабораторные

| № | Тема | Папка |
|---|------|-------|
| 1 | Dockerfile: плохой и хороший | [`lab1/`](lab1) |
| 2 | Docker Compose | [`lab2/`](lab2) |
| 3 | Kubernetes (minikube, Nextcloud + PostgreSQL) | [`lab3/`](lab3) |
| 4 | More Kubernetes: свой сервис | [`lab4/`](lab4) |

Задание лежит в `labN/docs/`.

## Как работаем

1. В `main` напрямую не пушим, туда попадает только то, что прошло ревью.
2. Каждая лаба делается в отдельной ветке от актуального `main`:
   ```bash
   git checkout main && git pull
   git checkout -b lab1   # lab2, lab3, lab4
   ```
3. Всё по лабе кладём в её папку, в `README.md` этой папки пишем отчёт.
4. Когда готово, пушим ветку и открываем Pull Request в `main`.
5. PR должен одобрить (Approve) хотя бы один другой участник команды, без аппрува не мержим.
6. Замечания из ревью исправляем коммитами в ту же ветку, после аппрува мержим, ветку удаляем.
