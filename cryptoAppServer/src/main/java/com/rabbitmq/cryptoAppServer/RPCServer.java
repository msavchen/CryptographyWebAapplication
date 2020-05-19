package com.rabbitmq.cryptoAppServer;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.InvalidParameterException;
import java.security.Key;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import com.rabbitmq.client.*;


//String message = Base64.getEncoder().encodeToString(macBytes);
public class RPCServer {

    private static final String RPC_QUEUE_NAME = "rpc_queue";
	private static Key key;

    private static byte[] mac(String algoPlain, Key key) {
    	Mac mac;
    	String[] messageSplitted = algoPlain.split(",", 2);
    	String algo = messageSplitted[0];
    	String plain = messageSplitted[1];
		try {
		    mac = Mac.getInstance(algo);
	    	mac.init(key);
	    	byte[] data = plain.getBytes("UTF-8");
	    	byte[] macBytes = mac.doFinal(data);	    	
	    	return Base64.getEncoder().encode(macBytes);
		} catch (NoSuchAlgorithmException | UnsupportedEncodingException | InvalidKeyException e) {
			e.printStackTrace();
			return Base64.getMimeDecoder().decode(e.getMessage());
		}
    }
    
    
    private static Key getKeyInstance(String algo, int keyBitSize) throws NoSuchAlgorithmException {
    	KeyGenerator keyGenerator;
		Key key = null;
		keyGenerator = KeyGenerator.getInstance(algo);
		SecureRandom secureRandom = new SecureRandom();
		keyGenerator.init(keyBitSize, secureRandom);
		key = keyGenerator.generateKey();
    	return key;	
    }
    
    private static Key dekey(String algo, String encodedKey) throws UnsupportedEncodingException {
    	byte[] decodedKey = encodedKey.getBytes("UTF-8");
    	Key originalKey = new SecretKeySpec(decodedKey, 0, decodedKey.length, algo);
    	return originalKey;
    }
    
    private static byte[] hash(String algoPlain) throws UnsupportedEncodingException{
    	String[] messageSplitted = algoPlain.split(",", 2);
    	String algo = messageSplitted[0];
    	String plain = messageSplitted[1];
    	byte[] data;
		try {
			data = plain.getBytes("UTF-8");
			MessageDigest messageDigest = MessageDigest.getInstance(algo);
	    	byte[] digest = messageDigest.digest(data);
	    	return Base64.getEncoder().encode(digest);
		} catch (UnsupportedEncodingException | NoSuchAlgorithmException e) {
			e.printStackTrace();
			return Base64.getMimeDecoder().decode(e.getMessage());
		}
    }
    
    private static byte[] encrypt(String algPlain, Key key) throws UnsupportedEncodingException {
    	String[] messageSplitted = algPlain.split(",", 2);
    	String algo = messageSplitted[0];
    	String plain = messageSplitted[1];
			try {
				Cipher cipher = Cipher.getInstance(algo);
				cipher.init(Cipher.ENCRYPT_MODE, key);
				byte[] plainText  = plain.getBytes("UTF-8");
				byte[] cipherText = cipher.doFinal(plainText);	
		        return Base64.getEncoder().encode(cipherText);
			} catch ( InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException | IllegalBlockSizeException | BadPaddingException e) {
				e.printStackTrace();
				return Base64.getMimeDecoder().decode(e.getMessage());
			}
    }
    
    private static byte[] decrypt(String algCiper, Key key) throws UnsupportedEncodingException {
    	String[] messageSplitted = algCiper.split(",", 2);
    	String algo = messageSplitted[0];
    	String ciphered = messageSplitted[1];
			try {
				Cipher cipher = Cipher.getInstance(algo);
				cipher.init(Cipher.DECRYPT_MODE, key);
				byte[] cipherText  = ciphered.getBytes("UTF-8");
				byte[] plainText = cipher.doFinal(cipherText);	 
		        return Base64.getEncoder().encode(plainText);
			} catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException | IllegalBlockSizeException | BadPaddingException e) {
				e.printStackTrace();
				return Base64.getMimeDecoder().decode(e.getMessage());
			}			
    }

    public static void main(String[] argv) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {
            channel.queueDeclare(RPC_QUEUE_NAME, false, false, false, null);
            channel.queuePurge(RPC_QUEUE_NAME);

            channel.basicQos(1);

            System.out.println(" [x] Awaiting RPC requests");

            final Object monitor = new Object();
            DeliverCallback deliverCallback = (consumerTag, delivery) -> {
                AMQP.BasicProperties replyProps = new AMQP.BasicProperties
                        .Builder()
                        .correlationId(delivery.getProperties().getCorrelationId())
                        .build();

                byte[] response = null;
                String algo;
                int keyBitSize;
				try {
                    String message = new String(delivery.getBody(), "UTF-8");
                    String[] messageSplitted = message.split(",", 2);
                    if (messageSplitted[0].equals("MAC")) {
                    	response = mac(messageSplitted[1], key); 
                    }
                    else if ((messageSplitted[0].equals("KEY"))){
                    	messageSplitted = messageSplitted[1].split(",", 2);
                    	algo = messageSplitted[0];
                    	keyBitSize = Integer.parseInt(messageSplitted[1]);
                    	try {
							key = getKeyInstance(algo, keyBitSize);
							response = Base64.getEncoder().encode(key.getEncoded());
						} catch (NoSuchAlgorithmException | InvalidParameterException e) {
							response = Base64.getMimeDecoder().decode(e.getMessage());
						} 
                    }   
                    else if ((messageSplitted[0].equals("HASH"))){
                    	response = hash(messageSplitted[1]);
                    } 
                    else if ((messageSplitted[0].equals("ENC"))){               
                    	response = encrypt(messageSplitted[1], key);                  	
                    }
                    else if ((messageSplitted[0].equals("DEC"))){                   	
                    	response = decrypt(messageSplitted[1], key);                   	
                    }
                    else if ((messageSplitted[0].equals("DEKEY"))){
                    	messageSplitted = messageSplitted[1].split(",", 2);
                    	algo = messageSplitted[0];
                    	key = dekey(algo, messageSplitted[1]);
                    	response = key.getEncoded();
                    }
                    System.out.println("resp:" + Base64.getEncoder().encodeToString(response));
                } catch (RuntimeException e) {
                    System.out.println(" [.] " + e.toString());
				} finally {
                    channel.basicPublish("", delivery.getProperties().getReplyTo(), replyProps, response);
                    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
                    synchronized (monitor) {
                        monitor.notify();
                    }
                }
            };

            channel.basicConsume(RPC_QUEUE_NAME, false, deliverCallback, (consumerTag -> { }));
            while (true) {
                synchronized (monitor) {
                    try {
                        monitor.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}