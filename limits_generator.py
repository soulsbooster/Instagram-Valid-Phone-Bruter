start_digits = input("Введите первые цифры для дапазонов ")
lines = int(input("Введите кол-во линий для разбития "))
start_limit = 1
end_limit = 9999999
threshold = 1000000
chunk = round(end_limit / lines)
chunk_amount = 0


def add_zero(digits):
    digits = str(digits)
    if len(digits) < len(str(threshold)):
        difference = len(str(threshold)) - len(digits)
        j = 1
        while j <= difference:
            digits = "0" + digits
            j += 1
    return digits


result = str(start_digits) + add_zero(1) + ':' + str(start_digits) + add_zero(chunk) + "\r\n"

chunk_amount += chunk
i = 1
while i < lines:
    start_chunk_amount = chunk_amount
    chunk_amount += chunk
    end_limit_digit = add_zero(chunk_amount)
    if int(end_limit_digit) > end_limit:
        end_limit_digit = str(end_limit)
    result += str(start_digits) + add_zero(start_chunk_amount) + ':' + str(start_digits) + \
        end_limit_digit + "\r\n"
    i += 1

print(result)

f = open("all_list.txt", "a")
f.write(result)
f.close()
