# LAB — день 4

> Это шаблон отчёта. Скопируйте его в `LAB.md` в корне вашего репозитория с ДЗ и заполните по ходу работы. Достаточно осмысленных заголовков, code-блоков с языком и ссылок на скриншоты.

Курс: [«Интенсив по погружению в GIT»](https://slurm.io/git-intensive)


## Базовая задача — `01-merge-vs-rebase`

### Стартовое состояние

Создана ветка `feat/perf-tuning`. В ветке `feat/perf-tuning` и `main` внесены и закомичены изменения в 4 файла: webapp/config.py webapp/services.py webapp/templates/index.html Dockerfile: одновременная настройка с противоположными целями одних и тех же функций. Обе ветки запущены в удаленный репозиторий.

```bash
# git log --oneline --graph --all (на момент окончания подготовки)
```

![Шаги до конфликта](screenshots/01-pre-merge-history.png)

### Путь A — через `merge`

[FIXME:Что сделано на ветке `experiment/merge`, какой файл и через что разрешали (CLI или VS Code Merge Editor). Какие компромиссы выбрали и почему.]
Создана ветка `experiment/merge` от последнего коммита в main и переключились на неё. В ветку влита `feat/perf-tuning` в режиме `merge`. Получены конфликты в 4 измененных файлах. С помощью VSCode разрешен конфликт в `webapp/config.py` и `webapp/services.py`, `Dockerfile` и `webapp/templates/index.html` разрешены в nano. Приняты изменения из `feat/perf-tuning`.

```bash
# ключевые команды
 git switch -c experiment/merge
 git merge feat/perf-tuning
 git mergetool 

 git add Dockerfile webapp/templates/index.html
 git commit -m "merge feat/perf-tuning: main commits"
 
```

![Состояние Merge Editor / CLI на момент конфликта](screenshots/02-merge-conflict.png)

![Финальный merge-коммит](screenshots/03-merge-result.png)

### Путь B — через `rebase`

Создана ветка `experiment/merge` от последнего коммита в main и переключились на неё. Влита ветка `feat/perf-tuning` в режиме rebase.

```
Auto-merging Dockerfile
CONFLICT (content): Merge conflict in Dockerfile
Auto-merging webapp/config.py
CONFLICT (content): Merge conflict in webapp/config.py
Auto-merging webapp/services.py
CONFLICT (content): Merge conflict in webapp/services.py
Auto-merging webapp/templates/index.html
CONFLICT (content): Merge conflict in webapp/templates/index.html
error: could not apply f232410... fix(prod): tighten timeouts, harden Dockerfile, add welcome banner
```

```bash
# ключевые команды
git switch main
git switch -c experiment/rebase
git rebase feat/perf-tuning
git mergetool
git log --merges --oneline experiment/rebase
git commit -am "rebase feat/perf-tuning"
```

![История после rebase](screenshots/04-rebase-result.png)

### Сравнение

Финальная история всех веток рядом:

![Сравнение историй experiment/merge vs experiment/rebase](screenshots/05-history-comparison.png)

Что я заметил(а) в процессе сравнения:
- нет merge коммита в rebase, история линейная
- ветка `feat/perf-tuning` видна в истории как сущность

### Какой подход я бы выбрал(а) в команде и почему

Для обновления `main` - merge, чтобы видеть как велась работа. В линейной истории после rebase теряется контекст.
Для вливания в свою ветку изменений из `main` - rebase.


## Задания со звездочкой (опционально)
> это заполняете только если делали. иначе не включайте в отчет и удалите их шаблона

### ⭐1 — `git pull` vs `git pull --rebase`

Что было воспроизведено, какая разница в истории получилась, какую глобальную настройку поставили в `~/.gitconfig`.
Создана ситуация, когда ветка изменена и локально, и на сервере.
В результате при `git fetch`, `git status` видим, что ветки разошлись.
Глобальная настройка pull.rebaseне занада, в результате получаем:
```
$ git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

Если сделать `git pull --merge`, то получаем ветвление, которое не всегда желательно - бессмыленный мусор в истории.
`git pull --rebase` переносит изменения с сервера и помещает локальный коммит на верх.
Для обеспечения этого поведения по умолчанию нужно изменить настройку конфигурации:
`git config --global pull.rebase true`.
Данное поведение по умолчанию применятся только на приватных ветках. **На публичных ветках rebase запрещен:** получается ситуация "отдай проблему соседу".
Опасность rebase на публичной ветке в том, что:
- переписывается история, которую кто-то мог увидеть
- другие разработчики при следующем pull --rebase тоже переписывают свои коммиты
- все коммиты меняют хеши → теряются ссылки, комментарии к PR, баг-трекеры
- у разных разработчиков оказываются разные версии "одних и тех же" коммитов

![Состояние истории до/после pull --rebase](screenshots/star-1-pull-rebase.png)

### ⭐2 — `--force-with-lease` vs `--force`

Что было сделано (`git commit --amend` после push), почему обычный `git push` отказал, чем `--force-with-lease` безопаснее `--force`.
```
$ git push
To github.com:sshopin/git-bootcamp-day-4.git
 ! [rejected]        chore/amend-demo -> chore/amend-demo (non-fast-forward)
error: failed to push some refs to 'github.com:sshopin/git-bootcamp-day-4.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

```
$ git push --force-with-lease
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 12 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 387 bytes | 129.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To github.com:sshopin/git-bootcamp-day-4.git
 + 9e7a808...3caed61 chore/amend-demo -> chore/amend-demo (forced update)
 ```

При наличии удаленного коммита:
```
$ git push --force-with-lease
To github.com:sshopin/git-bootcamp-day-4.git
 ! [rejected]        chore/amend-demo -> chore/amend-demo (stale info)
error: failed to push some refs to 'github.com:sshopin/git-bootcamp-day-4.git'
```

![Push --force-with-lease успех](screenshots/star-2-force-with-lease.png)

### ⭐3 — rebase с конфликтом на каждом коммите

Сюжет, через сколько `--continue` прошли, что почувствовали по сравнению с пассивным merge.

![Финал rebase --continue](screenshots/star-3-multi-conflict.png)

### ⭐4 — безопасный выход из detached HEAD

Как зашли в detached HEAD, какой коммит сделали, как выходили через `git switch -c`, чем `git reflog` помог как страховка.

![Выход из detached HEAD](screenshots/star-4-detached-head.png)

