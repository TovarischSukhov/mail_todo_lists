#encoding "utf-8"
#include 'np.cxx'

NeedWord -> 'надо' | 'нужен' | 'нужный' | 'нужно';

ToDoWord -> (NeedWord) AnyWord<kwtype='todo'>;

ToDoWord -> NeedWord (AnyWord<kwtype='todo'>);



Action_ -> Verb NP;

Action -> Action_ interp (CheckListFact.type);

GroupOfActions -> Action SimConjAnd GroupOfActions | Action Comma GroupOfActions | Action;

NPInterp -> NP interp (CheckListFact.type);
GroupOfNP -> NPInterp SimConjAnd GroupOfNP | NPInterp Comma GroupOfNP | NPInterp;

ToDoList -> ToDoWord (Word) (Word) GroupOfNP ;
ToDoList -> ToDoWord (AnyWord) (AnyWord) GroupOfActions+ ;
