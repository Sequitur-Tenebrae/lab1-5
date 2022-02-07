from automata.pda.npda import NPDA

import enum


class Rule(object):
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right


class Types(enum.Enum):
    zero = ('Тип 0', 0)
    context_sensitive = ('Контекстно-зависимая', 1)
    context_free = ('Контекстно-свободная', 2)
    left_regular = ('Лево-регулярная грамматика', 3)
    right_regular = ('Право-регулярная грамматика', 4)


class Grammar:
    def __init__(self, terms: set, non_terms: set, rules: set):
        self.terms = terms
        self.non_terms = non_terms
        self.rules = rules
        self.type = self.__get_type()

    def __is_term(self, symbol):
        return symbol in self.terms

    def __is_non_term(self, symbol):
        return symbol in self.non_terms

    def __is_regular(self, rule):
        if len(rule.left) != 1:
            return False
        if len(rule.right) == 1 and self.__is_non_term(rule.right[0]):
            return False
        if len(rule.right) == 2 and self.__is_non_term(rule.right[0]) and self.__is_non_term(rule.right[1]):
            return False
        if len(rule.right) == 2 and self.__is_term(rule.right[0]) and self.__is_term(rule.right[1]):
            return False

    def is_left_regular(self):
        for rule in self.rules:
            self.__is_regular(rule)
            if len(rule.right) == 2 and self.__is_non_term(rule.right[0]) and self.__is_term(rule.right[1]):
                return False
            if len(rule.right) == 1 and self.__is_non_term(rule.right):
                return False
        return True

    def is_right_regular(self):
        for rule in self.rules:
            self.__is_regular(rule)
            if len(rule.right) == 2 and self.__is_term(rule.right[0]) and self.__is_non_term(rule.right[1]):
                return False
            if len(rule.right) == 1 and self.__is_non_term(rule.right):
                return False
        return True

    def is_context_free(self):
        for rule in self.rules:
            if len(rule.left) != 1:
                return False
        return True

    def is_context_sensitive(self):
        for rule in self.rules:
            if len(rule.right) == 0:
                return False
            if len(rule.left) == 1:
                return False
        return True

    def __get_type(self):
        if self.is_left_regular():
            return Types.left_regular
        if self.is_right_regular():
            return Types.right_regular
        if self.is_context_free():
            return Types.context_free
        if self.is_context_sensitive():
            return Types.context_sensitive

if __name__ == '__main__':
    print('Input term:')
    terms = set(input())
    print('Input non_term:')
    non_terms = set(input())
    print('Input rule:')
    rules = input()
    rules = rules.split(',')
    rule_set = set()
    for rule in rules:
        parts = rule.split('->')
        left = parts[0]
        right = parts[1]
        right = right.split('|')
        for r in right:
            rule_set.add(Rule(left, r))
    grammar = Grammar(terms, non_terms, rule_set)
    if grammar.type.value[1] < Types.context_free.value[1]:
        print('Ошибка! Была введена не КС грамматика')
        exit(0)
    print('Введите строку для проверки МП-автоматом:')
    s = input()
    transitions = dict()
    transitions['q'] = dict()
    transitions['q'][''] = {x: set() for x in grammar.non_terms}
    for rule in grammar.rules:
        transitions['q'][''][rule.left].add(('q', tuple(rule.right)))
    for term in grammar.terms:
        transitions['q'][term] = {term: {('q', '')}}
    npda = NPDA(
        states={'q'},
        input_symbols=grammar.terms,
        stack_symbols=list(grammar.terms | grammar.non_terms),
        transitions=transitions,
        initial_state='q',
        initial_stack_symbol='S',#меняем на первый символ строки rule
        final_states={'q'},
        acceptance_mode='empty_stack'
    )

    if npda.accepts_input(s):
        print('Строка принята полностью')
        print('Введите строку для проверки расширенным МП-автоматом:')
        ss = input()
        transitions = dict()
        transitions['q'] = dict()
        transitions['q'][''] = {x: set() for x in grammar.non_terms}
        for rule in grammar.rules:
            transitions['q'][''][rule.left].add(('q', tuple(rule.right)))
        for term in grammar.terms:
            transitions['q'][term] = {term: {('q', '')}}
        npda = NPDA(
            states={'q'},
            input_symbols=grammar.terms,
            stack_symbols=list(grammar.terms | grammar.non_terms),
            transitions=transitions,
            initial_state='q',
            initial_stack_symbol='S',#меняем на первый символ строки rule
            final_states={'q'},
            acceptance_mode='final_state'
        )
        if npda.accepts_input(ss):
            print('Строка принята полностью')
