generate_bin:
	gcc -o generate_bin -I headers generate_bin.c

clean:
	rm -f generate_bin message_data.bin

exe:	
	./generate_bin

all: clean generate_bin exe
