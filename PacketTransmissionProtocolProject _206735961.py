#Lidor Pahima 
#Packet Class - Represents a packet that will be sent from the sender to the receiver.
class Packet:
    # Constructor - Initializes the packet with the source address, destination address, sequence number, is_ack and data.
    def __init__(self, source_address, destination_address, sequence_number,
                 is_ack=False, data=None):
        self.__source_address = source_address
        self.__destination_address = destination_address
        self.__sequence_number = sequence_number
        self.__is_ack = is_ack
        self.__data = data
    # Returns a string representation of the packet.
    def __repr__(self):
        return "Packet(Source IP: " + self.__source_address \
                    + ", Dest: " + self.__destination_address \
                    + ", #Seq: " + str(self.__sequence_number) \
                    + ", ACK: " + str(self.__is_ack) \
                    + ", Data: " + str(self.__data) + ")"
                    
    # Returns the source address of the packet.
    def get_source_address(self):
        return self.__source_address
    
    # Returns the destination address of the packet.
    def get_destination_address(self):
        return self.__destination_address
    
    # Returns the sequence number of the packet.
    def get_sequence_number(self):
        return self.__sequence_number
    
    # Sets the sequence number of the packet.
    def set_sequence_number(self, seq_num):
        self.__sequence_number = seq_num
        
    # Returns whether the packet is an acknowledgment packet.
    def get_is_ack(self):
        return self.__is_ack
    # Returns the data of the packet.
    def get_data(self):
        return self.__data
    
# Communicator Class - Represents a communicator that can send and receive packets.
class Communicator:
    def __init__(self, address):
        self.__address = address
        self.__current_sequence_number = None
        
    # Returns the address of the communicator.
    def get_address(self):
        return self.__address

    # Returns the current sequence number of the communicator.
    def get_current_sequence_number(self):
        return self.__current_sequence_number
    
    # Sets the current sequence number of the communicator.
    def set_current_sequence_number(self, seq_num):
        self.__current_sequence_number = seq_num
       
    # Sends a packet to the receiver.
    def send_packet(self, packet):
        print("Sender: Packet Seq Num:", packet.get_sequence_number())
        return packet

    # increments the current sequence number by 1.
    def increment_current_seq_num(self):
        self.set_current_sequence_number(self.get_current_sequence_number() + 1)

# Sender Class - Represents a sender that can send packets to a receiver.
class Sender(Communicator):
    # Constructor - Initializes the sender with the address and the number of letters in a packet.
    def __init__(self, address, num_letters_in_packet):
        self.__address = address
        self.__num_letters_in_packet = num_letters_in_packet

    # Prepares the packets to be sent to the receiver.
    def prepare_packets(self, message, destination_address):
        packets = [] #  list of packets
        packet_size = self.__num_letters_in_packet # packet size
   
        FillMessage = message.ljust(((len(message) + packet_size - 1) // packet_size) * packet_size) # fill the message with spaces 
        Sequence = 0
        for i in range(0, len(FillMessage), packet_size): # loop over the message and create packets
            packet_data = FillMessage[i:i+packet_size]  # get the data of the packet
            packets.append(Packet(source_address=self.__address, destination_address=destination_address, sequence_number=Sequence, data=packet_data)) # create the packet
            Sequence += 1 # increment the sequence number
        return packets # return the packets
        
    # Receives an acknowledgment packet from the receiver.
    def receive_ack(self, acknowledgment_packet):
        return acknowledgment_packet.get_is_ack()

# Receiver Class - Represents a receiver that can receive packets from a sender.
class Receiver(Communicator):
    # Constructor - Initializes the receiver with the address and an empty list of received packets.
    def __init__(self, address):
        super().__init__(address)
        self.__packets_received = []
 
    # Receives a packet from the sender.
    def receive_packet(self, packet):
        self.__packets_received.append(packet) # add the packet to the list of received packets
        print("Receiver: Received packet seq num:", packet.get_sequence_number()) 
        ack_packet = Packet(source_address=packet.get_destination_address(),  # create an acknowledgment packet
                        destination_address=packet.get_source_address(),
                        sequence_number=packet.get_sequence_number(),
                        is_ack=True,
                        data=None)
    
        return ack_packet   # return the acknowledgment packet to the sender 

    # Returns the message by concatenating the data of the received packets.
    def get_message_by_received_packets(self):
        full_message = "".join(packet.get_data() for packet in self.__packets_received)
        return full_message

if __name__ == '__main__':
    source_address = "192.168.1.1"
    destination_address = "192.168.2.2"
    message = "What is up?"
    num_letters_in_packet = 3

    sender = Sender(source_address, num_letters_in_packet)
    receiver = Receiver(destination_address)

    packets = sender.prepare_packets(message, receiver.get_address())

    # setting current packet
    start_interval_index = packets[0].get_sequence_number()
    # setting current packet in the sender and receiver
    sender.set_current_sequence_number(start_interval_index)
    receiver.set_current_sequence_number(start_interval_index)

    # setting the last packet
    last_packet_sequence_num = packets[-1].get_sequence_number()
    receiver_current_packet = receiver.get_current_sequence_number()

    while receiver_current_packet <= last_packet_sequence_num:
        current_index = sender.get_current_sequence_number()
        packet = packets[current_index]
        packet = sender.send_packet(packet)

        ack = receiver.receive_packet(packet)

        result = sender.receive_ack(ack)

        if result == True:

            sender.increment_current_seq_num()
            receiver.increment_current_seq_num()

        receiver_current_packet = receiver.get_current_sequence_number()

    full_message = receiver.get_message_by_received_packets()
    print(f"Receiver message: {full_message}")