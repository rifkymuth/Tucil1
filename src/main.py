import time
import re
import os.path

alphabet_sets = []
operand_words = []
result_word = []
first_letters = []
list_permutasi = []


# load data file
def load_data(file_name):
    f = open(os.path.dirname(__file__)+file_name, "r")
    contents = f.read()
    lines = contents.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip(" +")
    for i in range(len(lines)):
        if (lines[i][0] == "-"):
            for j in range(i):
                operand_words.append(list(lines[j]))
            for k in range(len(lines[-1])):
                result_word.append(lines[-1][k])
            break

    # searching first letters
    for word in operand_words:
        if not word[0] in first_letters:
            first_letters.append(word[0])
    if not result_word[0] in first_letters:
        first_letters.append(result_word[0])

    # creating alphabet set
    for word in operand_words:
        for i in range(len(word)):
            if not word[i] in alphabet_sets:
                alphabet_sets.append(word[i])
    for letter in result_word:
        if not letter in alphabet_sets:
            alphabet_sets.append(letter)


# permutation of 0-9 numbers
def permutasi(numset):
    if len(numset) == 1:
        return [numset]

    numset_next = permutasi(numset[1:])
    x = numset[0]
    perm = []
    for p in numset_next:
        for i in range(len(p)+1):
            perm.append(p[:i] + x + p[i:])
    return perm


# checking permutation solutions
def cryptarithmetic(alphabetsets, operandwords, resultword):
    time_start = time.time()
    n_case = 0
    for iterable in list_permutasi:
        current_alphabet_sets = alphabetsets.copy()
        current_operand_words = operandwords.copy()
        current_result_word = resultword.copy()
        permutasi_set = list(iterable)

        # creating dictionary to swap letter to number
        swap_dict = {}

        skip = False
        for i in range(len(alphabet_sets)):
            # eliminate first letters that are 0
            if (permutasi_set[i] == '0' and (current_alphabet_sets[i] in first_letters)):
                skip = True

            # first letters are not 0
            else:
                swap_dict[current_alphabet_sets[i]] = permutasi_set[i]

        if not skip:
            # swapping operand letters and result letters to number
            for i in range(len(current_operand_words)):
                current_operand_words[i] = [swap_dict.get(x, x)
                                            for x in current_operand_words[i]]
            current_result_word = [swap_dict.get(
                x, x) for x in current_result_word]

            # checking
            n_case += 1
            operand_sum = 0
            result_int = 0
            for i in range(len(current_operand_words)):
                operand_sum += int("".join(current_operand_words[i]))
            result_int = int("".join(current_result_word))

            # permutation satisfies
            if (operand_sum == result_int):
                print("    Permasalahan test case:")
                print()
                for word in operand_words:
                    print("    {:>10s}".format("".join(word)))
                print("    ---------- +")
                print("    {:>10s}".format("".join(result_word)))
                print()

                print("    Solusi:")
                print()
                for word in current_operand_words:
                    print("    {:>10s}".format("".join(word)))
                print("    ---------- +")
                print("    {:>10s}".format("".join(current_result_word)))
                print()

                print("    Tuple solusi -> ", swap_dict)
                print("    Case number:", n_case)
                time_end = time.time()
                print("    Durasi: {:.3f} seconds".format(
                    time_end - time_start))
                break


def print_greetings():
    print("     ------------------------------------------------------------")
    print("     ------------- WELCOME TO CRYPTARITMETIC SOLVER -------------")
    print("     ------------------------------------------------------------")


def print_menu():
    print()
    print("     Silakan pilih menu:")
    print("     1 - 8 : test case 1 - 8")
    print("     9     : keluar")
    print()


# main program
print_greetings()
active = True
while active:
    allowed_menu_inputs = "[1-9]"
    print_menu()
    while True:
        # try:
        user_input = str(input("    input  : ")).strip()
        if not re.match(allowed_menu_inputs, user_input):
            print("    Pilih angka antara 1-9!")
        else:
            break
        # except:
        print("    Input tidak sesuai!")

    if (user_input != "9"):
        print()
        print("    Memuat data test . . .")
        print()

        file_path = "/../test/test" + user_input + ".txt"
        load_data(file_path)
        for item in permutasi("0123456789"):
            list_permutasi.append(''.join(list(item)[:len(alphabet_sets)]))
        list_permutasi = list(set(list_permutasi))
        cryptarithmetic(alphabet_sets, operand_words, result_word)
        alphabet_sets.clear()
        operand_words.clear()
        result_word.clear()
        first_letters.clear()
        list_permutasi.clear()
    else:
        print("    Terima kasih telah menggunakan solver ini!")
        active = False
