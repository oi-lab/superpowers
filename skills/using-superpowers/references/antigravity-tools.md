# Correspondance des outils de la CLI Antigravity (`agy`)

Les skills parlent en actions (« dispatcher un sous-agent », « créer un todo », « lire un fichier »). Sur la CLI Antigravity (`agy`), elles se résolvent vers les outils ci-dessous.

| Action demandée par le skill | Équivalent CLI Antigravity |
|----------------------|----------------------|
| Dispatcher un sous-agent (gabarit `Subagent (general-purpose):`) | `invoke_subagent` avec un `TypeName` intégré — `self` pour du travail à pleines capacités, `research` pour de la lecture seule |
| Suivi de tâches (« créer un todo », « marquer terminé ») | un **artefact task** — `write_to_file` avec `IsArtifact: true` et `ArtifactType: "task"` (voir [Suivi de tâches](#suivi-de-tâches)). **Pas** `manage_task`, qui gère les processus en arrière-plan. |

## Suivi de tâches

Antigravity n'a **aucun outil de todo** (`manage_task` gère les processus en
arrière-plan — `list`/`kill`/`status`/`send_input` — ce n'est *pas* une checklist). Quand un
skill dit de créer une liste de todos ou de suivre des tâches, maintiens un **artefact task** : une
checklist markdown sauvegardée avec `write_to_file` (`IsArtifact: true`,
`ArtifactMetadata.ArtifactType: "task"`), éditée avec `replace_file_content` /
`multi_replace_file_content` au fur et à mesure.

Au début de toute tâche multi-étapes, crée l'artefact task listant chaque étape de
ton plan. À mesure que tu termines une étape, édite l'artefact pour la marquer faite (`- [x]`).
Si le plan change, mets la checklist à jour. Garde-la à jour — c'est ta source de
vérité de ce qui reste ; une fois la conversation longue, relis-la avant de commencer
chaque étape.
