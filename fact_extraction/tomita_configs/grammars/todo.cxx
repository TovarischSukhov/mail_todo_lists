#encoding "utf-8"

NeedWord -> 'надо' | 'нужен' | 'нужна';

ToDoWord -> (NeedWord) AnyWord<kwtype='todo'>;

ToDoWord -> NeedWord (AnyWord<kwtype='todo'>) | Verb;

NP -> Noun;

ToDoList -> ToDoWord (Verb) NP+ interp (CheckListFact.type);
