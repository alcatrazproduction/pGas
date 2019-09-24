/*     */ package jgas;
/*     */ 
/*     */ public class MessungRead implements SerialPortEventListener {
/*     */   private InputStream inputStream;
/*     */   private BufferedReader bufferedReader;
/*     */   private SerialPort serialPort;
/*     */   private MessungReadThread readThread;
/*     */   private boolean dataRead;
/*     */   private char commandChar;
/*     */   private String applicationName;
/*     */   private StringBuffer messung;
/*     */   private OutputStream messungTextOutputStream;
/*     */   private Vector listeners;
/*     */   
/*     */   private class MessuangReadThread extends Thread {
/*     */     public static final int PAUSE = 1;
/*     */     public static final int WAITING = 2;
/*     */     public static final int NOTIFY = 3;
/*     */     private boolean read;
/*     */     
/*     */     public MessungReadThread(int waitTime, MessungRead parent) {
/*  22 */       this.read = false;
/*     */ 
/*     */       
/*  25 */       this.running = true;
/*  26 */       this.status = 1;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */       
/*  32 */       this.waitTime = waitTime;
/*  33 */       this.parent = parent;
/*  34 */       this; setPriority(1);
/*  35 */       start();
/*     */     }
/*     */     private int waitTime; private MessungRead parent; private boolean running; private int status;
/*     */     
/*     */     public void run() {
/*  40 */       while (this.running) {
/*     */         
/*  42 */         switch (this.status) {
/*     */           
/*     */           case 1:
/*  45 */             if (this.read) {
/*     */               
/*  47 */               this.parent.notifyMessungBegin();
/*  48 */               this.status = 2;
/*  49 */               this.read = true; continue;
/*     */             } 
/*     */             try {
/*  52 */               Thread.sleep(200L);
/*  53 */             } catch (InterruptedException e) {}
/*     */ 
/*     */ 
/*     */ 
/*     */           
/*     */           case 2:
/*     */             try {
/*  60 */               Thread.sleep(this.waitTime);
/*  61 */             } catch (InterruptedException e) {}
/*     */             
/*  63 */             if (this.read) {
/*  64 */               this.status = 2;
/*  65 */               this.read = false; continue;
/*     */             } 
/*  67 */             this.status = 3;
/*  68 */             this.read = true;
/*     */ 
/*     */ 
/*     */ 
/*     */           
/*     */           case 3:
/*  74 */             this.parent.notifyMessungEnde();
/*  75 */             this.status = 1;
/*  76 */             this.read = false;
/*     */         } 
/*     */       } 
/*     */     }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */     
/*  85 */     public void end() { this.running = false; }
/*     */ 
/*     */ 
/*     */ 
/*     */     
/*  90 */     public void setRead() { this.read = true; }
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static void main(String[] args) {
/* 115 */     String defaultPort = "COM4";
/*     */ 
/*     */     
/* 118 */     if (args.length > 0) {
/* 119 */       defaultPort = args[0];
/*     */     }
/*     */     
/*     */     try {
/* 123 */       MessungRead mess = new MessungRead(defaultPort, "J-Gas Test", 2000, System.out);
/* 124 */       mess.startRead();
/* 125 */     } catch (PortInUseException e) {
/* 126 */       System.out.println(e);
/* 127 */     } catch (NoSuchPortException e) {
/* 128 */       System.out.println(e);
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public MessungRead(String SerialPortName, String applicationName, int timeOut, OutputStream resultOutputStream) throws PortInUseException, NoSuchPortException {
/*     */     this.dataRead = true;
/*     */     this.commandChar = 'D';
/*     */     this.applicationName = "J-Gas";
/*     */     this.messung = new StringBuffer();
/*     */     this.listeners = new Vector();
/* 144 */     this.applicationName = applicationName;
/* 145 */     this.messungTextOutputStream = resultOutputStream;
/*     */     
/* 147 */     this.readThread = new MessungReadThread(timeOut, this);
/*     */     
/*     */     try {
/* 150 */       CommPortIdentifier portId = CommPortIdentifier.getPortIdentifier(SerialPortName);
/*     */       
/* 152 */       this.serialPort = (SerialPort)portId.open(applicationName, 2000);
/*     */       
/* 154 */       this.serialPort.setSerialPortParams(1200, 8, 1, 0);
/*     */ 
/*     */ 
/*     */       
/* 158 */       this.inputStream = this.serialPort.getInputStream();
/*     */       
/* 160 */       this.serialPort.addEventListener(this);
/* 161 */       this.serialPort.notifyOnDataAvailable(true);
/*     */     }
/* 163 */     catch (UnsupportedCommOperationException e) {
/* 164 */       LogManager.getLogger().error("Serial Port opening not Supported", e);
/* 165 */     } catch (IOException e) {
/* 166 */       LogManager.getLogger().error("Serial Port communication error", e);
/* 167 */     } catch (TooManyListenersException e) {
/* 168 */       LogManager.getLogger().error("Serial Port event error", e);
/*     */     } 
/*     */   }
/*     */ 
/*     */   
/*     */   public void finalize() {
/*     */     try {
/* 175 */       this.serialPort.getOutputStream().close();
/* 176 */       this.inputStream.close();
/* 177 */       this.readThread.end();
/* 178 */     } catch (IOException e) {}
/*     */   }
/*     */ 
/*     */ 
/*     */   
/*     */   public void startRead() {
/*     */     try {
/* 185 */       this.serialPort.getOutputStream().write(68);
/* 186 */       this.serialPort.getOutputStream().flush();
/* 187 */     } catch (IOException e) {
/* 188 */       LogManager.getLogger().error("Error startign Read Thread", e);
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void serialEvent(SerialPortEvent event) {
/*     */     byte[] readBuffer;
/* 197 */     switch (event.getEventType()) {
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */       
/*     */       case 1:
/* 219 */         this.readThread.setRead();
/* 220 */         LogManager.getLogger().debug("COM: Data at COM");
/*     */         
/* 222 */         readBuffer = new byte[20];
/*     */         try {
/* 224 */           while (this.inputStream.available() > 0) {
/* 225 */             readBuffer = new byte[20];
/* 226 */             int numBytes = this.inputStream.read(readBuffer);
/* 227 */             LogManager.getLogger().debug("COM: Read number of bytes: " + (new Integer(numBytes)).toString());
/* 228 */             this.messungTextOutputStream.write(readBuffer);
/* 229 */             LogManager.getLogger().debug("COM: Add Data to buffer: " + new String(readBuffer));
/* 230 */             this.messung.append(readBuffer);
/*     */           } 
/*     */ 
/*     */ 
/*     */           
/* 235 */           this.messungTextOutputStream.flush();
/* 236 */         } catch (IOException e) {
/* 237 */           LogManager.getLogger().error("COM: Read Error", e);
/*     */         } 
/*     */         break;
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/* 250 */   public void addMessungListener(MessungListener listener) { this.listeners.addElement(listener); }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/* 258 */   public void removeMessungListener(MessungListener listener) { this.listeners.removeElement(listener); }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   protected void notifyMessung(MessungEvent e) {
/* 266 */     Enumeration listenersEnum = this.listeners.elements();
/* 267 */     while (listenersEnum.hasMoreElements())
/*     */     {
/* 269 */       ((MessungListener)listenersEnum.nextElement()).messungReceived(e);
/*     */     }
/* 271 */     this.messung.delete(0, this.messung.length());
/*     */   }
/*     */ 
/*     */ 
/*     */   
/* 276 */   protected void notifyMessungEnde() { notifyMessung(new MessungEvent(this, this.messung.toString(), 2)); }
/*     */ 
/*     */ 
/*     */ 
/*     */   
/* 281 */   protected void notifyMessungBegin() { notifyMessung(new MessungEvent(this, this.messung.toString(), 1)); }
/*     */ }


/* Location:              C:\Program Files (x86)\J-Gas\J-Gas.jar!\jgas\MessungRead.class
 * Java compiler version: 5 (49.0)
 * JD-Core Version:       1.0.7
 */
