def my_inappropriately_named_function(num):
    if num > 1:
        my_inappropriately_named_function(num // 2)
    print (num % 2, end='\n')


number = int(input( "Enter an integer: "))
my_inappropriately_named_function(number)