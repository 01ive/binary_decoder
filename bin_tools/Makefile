generate_bin:
	gcc -o generate_bin -I headers generate_bin.c

send_bin:
	gcc -o send_bin send_bin.c

clean:
	rm -f generate_bin send_bin message_data.bin

generate:	
	./generate_bin

send:	
	./send_bin

all: clean generate_bin send_bin generate send
