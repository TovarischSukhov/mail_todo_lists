#encoding "utf-8"
#include 'np.cxx'

NeedWord -> 'надо' | 'нужен' | 'нужный' | 'нужно';

ToDoWord -> (NeedWord) AnyWord<kwtype='todo'>;

ToDoWord -> NeedWord (AnyWord<kwtype='todo'>);

//NP -> NP Comma | NP SimConjAnd;

Action_ -> Verb NP;
//Action_ -> Verb NP Comma NP;
//Action_ -> Verb NP SimConjAnd NP;

Action -> Action_ interp (CheckListFact.type);

GroupOfActions -> Action SimConjAnd GroupOfActions | Action Comma GroupOfActions | Action;

ToDoList -> ToDoWord NP interp (CheckListFact.type);
ToDoList -> NeedWord (AnyWord) (AnyWord) GroupOfActions+ ;
