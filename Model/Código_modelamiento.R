######## Correlaciones de Pearson ###########################################################################################################
######## Calcula las correlaciones de Pearson para todo par de variables (incluyendo la respuesta) y realiza gr�ficos de dispersi�n de cada
######## variable explicativa frente a la respuesta. Los par�metros de la funci�n  Correlaciones(objeto,a,b,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. a. N�mero de filas de gr�ficos
######## 3. b. N�mero de columnas de gr�ficos
######## 4. d. N�mero de observaciones que se quieren identificar en cada diagrama de dispersi�n.
######## 5. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

Correlaciones <- function(objeto,a,b,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)
  }
  X <- model.matrix(objeto)
  if(mean(X[,1])==1){
    p <- ncol(model.matrix(objeto))
    labels <- labels(coef(objeto))
    respuesta <- names(objeto$model[1])
    par(mfrow=c(a,b))
    for(i in 2:p){
      plot(X[,i], y, main=labels[i], xlab=labels[i], ylim=c(min(y),max(y)), ylab=respuesta, cex=0.3, lwd=3)
      abline(lm(y~1+X[,i]),0,lty=3)
      identify(X[,i], y, n=d, labels=nombres)
    }
    resultado <- cor(cbind(objeto$model))
  }
  
  if(mean(X[,1])!=1){
    p <- ncol(model.matrix(objeto))
    labels <- labels(coef(objeto))
    respuesta <- names(objeto$model[1])
    par(mfrow=c(a,b))
    for(i in 1:p){
      plot(X[,i], y, main=labels[i], xlab=labels[i], ylim=c(min(y),max(y)), ylab=respuesta, cex=0.3, lwd=3)
      abline(lm(y~1+X[,i]),0,lty=3)
      identify(X[,i], y, n=d, labels=nombres)
    }
    resultado <- cor(cbind(objeto$model))
  }
  resultado
}


######## Correlaciones Parciales ###########################################################################################################
######## Calcula las correlaciones Parciales para cada variable explicativa frente a la respuesta y realiza un gr�fico de dispersi�n con los
######## resultados. Los par�metros de la funci�n Correlaciones.parcial(objeto,a,b,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. a. N�mero de filas de gr�ficos
######## 3. b. N�mero de columnas de gr�ficos
######## 4. d. N�mero de observaciones que se quieren identificar en cada diagrama de dispersi�n.
######## 5. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

Correlaciones.parcial <- function(objeto,a,b,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)
  }
  X <- model.matrix(objeto)
  if(mean(X[,1])==1){
    p <- ncol(model.matrix(objeto))
    labels <- labels(coef(objeto))
    respuesta <- names(objeto$model[1])
    resultado <- matrix(0,p-1,1)
    par(mfrow=c(a,b))
    for(i in 2:p){
      temporal1 <- glm(y ~ -1+X[,-i], family=gaussian())
      r1 <- y - fitted(temporal1)
      temporal2 <- glm(X[,i] ~ -1+X[,-i], family=gaussian())
      r2 <- X[,i] - fitted(temporal2)
      plot(r2, r1, main=labels[i], xlab=labels[i], ylab=respuesta, cex=0.3, lwd=3)
      abline(lm(r1~1+r2),0,lty=3)
      identify(r2, r1, n=d, labels=nombres)
      resultado[i-1] <- round(cor(r1,r2),3) 
    }
    resultado <- rbind(c("Variables","Respuesta"),cbind(labels[2:p],resultado))
  }
  
  if(mean(X[,1])!=1){
    p <- ncol(model.matrix(objeto))
    labels <- labels(coef(objeto))
    respuesta <- names(objeto$model[1])
    resultado <- matrix(0,p,1)
    par(mfrow=c(a,b))
    for(i in 1:p){
      temporal1 <- glm(y ~ 1+X[,-i], family=gaussian())
      r1 <- y - fitted(temporal1)
      temporal2 <- glm(X[,i] ~ 1+X[,-i], family=gaussian())
      r2 <- X[,i] - fitted(temporal2)
      plot(r2, r1, main=labels[i], xlab=labels[i], ylab=respuesta, cex=0.3, lwd=3)
      abline(lm(r1~1+r2),0,lty=3)
      identify(r2, r1, n=d, labels=nombres)
      resultado[i] <- round(cor(r1,r2),3) 
    }
    resultado <- rbind(c("Variables","Correlaci�n parcial con la respuesta"),cbind(labels[1:p],resultado))
  }
  resultado
}

######## Busqueda del "mejor" modelo ###########################################################################################################
######## Calcula las medidas de la calidad del ajuste SCRes, R2, R2 Ajustado y AIC para todas las combinaciones de modelos con i variables
######## explicativas. Los par�metros de la funci�n ajuste.normal(objeto,i) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. i. El n�mero de variables explicativas que se quieren en el modelo.

ajuste.normal <- function(objeto,i){
  y <- objeto$residuals + fitted(objeto)
  X <- model.matrix(objeto)
  p <- ncol(model.matrix(objeto))
  labels <- labels(coef(objeto))
  weights=objeto$weights
  if(length(weights)<length(y)){
    weights <- matrix(1,length(y),1)
  }
  if(mean(X[,1])==1){
    id <- seq(2,p,by=1)
    opcion <- t(combn(id,i))
    nn <- matrix(0,nrow(opcion),4)
    lab <- matrix(0,nrow(opcion),i+1)
    for(j in 1:nrow(opcion)){
      temp <- glm(y ~ 1+X[,opcion[j,]], family=gaussian(), weights=weights)
      mr <- (length(y)-1)*var(y)
      nn[j,4] <- round(AIC(temp),1)
      r2 <- (mr-sum((temp$y-fitted(temp))^2))/mr
      nn[j,3] <- round(1-(1-r2)*((length(y)-1)/(length(y)-1-i)),3)
      nn[j,1] <- round(sum((temp$y-fitted(temp))^2),1)
      nn[j,2] <- round(r2,3)
      lab[j,] <- labels[c(1,opcion[j,])]
    }
    lab2 <- matrix("",1,i+1)
    nn2 <- cbind("SCRes","R2","R2 Ajust","AIC")
    lab2[1] <- "Modelo"
    nn <- rbind(nn2,nn)
    lab <- rbind(lab2,lab)
    resultados <- cbind(lab,nn)
  }
  if(mean(X[,1])!=1){
    id <- seq(1,p,by=1)
    opcion <- t(combn(id,i))
    nn <- matrix(0,nrow(opcion),4)
    lab <- matrix(0,nrow(opcion),i)
    for(j in 1:nrow(opcion)){
      temp <- glm(y ~ -1+X[,opcion[j,]], family=gaussian(), weights=weights)
      mr <- sum(y*y)
      nn[j,4] <- round(AIC(temp),1)
      r2 <- (mr-sum((temp$y-fitted(temp))^2))/mr
      nn[j,3] <- round(1-(1-r2)*((length(y)-1)/(length(y)-1-i)),3)
      nn[j,1] <- round(sum((temp$y-fitted(temp))^2),1)
      nn[j,2] <- round(r2,3)   
      lab[j,] <- labels[opcion[j,]]
    }
    lab2 <- matrix("",1,i)
    nn2 <- cbind("SCRes","R2","R2 Ajust","AIC")
    lab2[1] <- "Modelo"
    nn <- rbind(nn2,nn)
    lab <- rbind(lab2,lab)
    resultados <- cbind(lab,nn)
  }
  resultados
}


######## Identificando puntos de alto Leverage ###################################################################################################################
######## Calcula los valores de la diagonal principal de la matriz de proyecci�n ortogonal H.
######## Los par�metros de la funci�n Leverage.normal(objeto,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. d. N�mero de observaciones que se quieren identificar.
######## 3. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

Leverage.normal <- function(objeto,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)
  }
  H <- matrix(0,length(y),1)
  X <- model.matrix(objeto)
  sigma2 <- sum(objeto$residuals^2)/(length(y)-ncol(X))
  XtX <- vcov(objeto)/sigma2
  for(i in 1:length(y)){
    H[i] <- t(X[i,])%*%XtX%*%X[i,]
  }
  maxy <- max(max(H),2*mean(H))
  plot(H, main="Puntos de alto Leverage", xlab="�ndice", ylim=c(0,maxy), ylab="h", cex=0.3, lwd=3)
  abline(2*mean(H),0,lty=3)
  identify(H, n=d,labels=nombres)
  H
}


######## Residuos Estandarizados ###############################################################################################################
######## Construye el gr�fico de residuos est�ndarizados del modelo. Los par�metros de la funci�n Residuos.normal(objeto,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. d. N�mero de observaciones que se quieren identificar.
######## 3. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

Residuos.normal <- function(objeto,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  h <- matrix(0,length(y),1)
  X <- model.matrix(objeto)
  sigma <- sum(objeto$residuals^2)/(length(y)-ncol(X))
  XtX <- vcov(objeto)/sigma
  for(i in 1:length(y)){
    h[i] <- t(X[i,])%*%XtX%*%X[i,]
  }
  r <- (y-fitted(objeto))/sqrt((1-h)*sigma)
  r <- r*sqrt((length(y)-ncol(X)-1)/(length(y)-ncol(X)-r*r))
  maxy <- max(max(r),3)
  miny <- min(min(r),-3)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)
  }
  plot(fitted(objeto), r, main="Observaciones extremas en la respuesta", xlab="Media estimada", ylab="Residuo estandarizado", cex=0.3, lwd=3, ylim=c(miny,maxy))
  abline(2,0,lty=3)
  abline(0,0,lty=3)
  abline(-2,0,lty=3)
  identify(x=fitted(objeto), y=r, n=d, labels=nombres)
  r
}



######## QQ Plot y sus bandas de confianza ###################################################################################################################
######## Construye el gr�fico QQ plot junto con sus bandas de confianza. Los par�metros de la funci�n qqplot.normal(objeto,k,alfa,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. d. N�mero de r�plicas para la simulaci�n.
######## 3. alpha. El nivel de confianza para las bandas del QQ plot es de 100*(1-alpha)%.
######## 4. d. N�mero de observaciones que se quieren identificar.
######## 5. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

qqplot.normal <- function(objeto,k,alfa,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)
  }
  y <- objeto$residuals + fitted(objeto)
  X <- model.matrix(objeto)
  n <- nrow(X)
  p <- ncol(X)
  phi <- sum(objeto$residuals*objeto$residuals)/(length(y)-length(coef(objeto)))
  XtX <- vcov(objeto)/phi
  h <- matrix(0,length(y),1)
  for(i in 1:length(y)){
    h[i] <- t(X[i,])%*%XtX%*%X[i,]
  }
  r <- (y-fitted(objeto))/sqrt((1-h)*phi)
  r <- r*sqrt((length(y)-ncol(X)-1)/(length(y)-ncol(X)-r*r))
  alfa1 <- ceiling(k*alfa)
  alfa2 <- ceiling(k*(1-alfa))
  epsilon <- matrix(0,n,k)
  e <- matrix(0,n,k)
  e1 <- numeric(n)
  e2 <- numeric(n)
  
  for(i in 1:k){
    resp <- fitted(objeto) + rnorm(n,mean=0,sd=1)*sqrt(phi) 
    fits <- glm(resp ~ X, family=gaussian())
    phis <- sum(fits$residuals*fits$residuals)/(length(y)-length(coef(fits)))
    rs <- (resp-fitted(fits))/sqrt((1-h)*phis)
    rs <- rs*sqrt((length(y)-ncol(X)-1)/(length(y)-ncol(X)-rs*rs))
    e[,i] <- sort(rs)
  }
  med <- apply(e,1,mean)
  
  for(i in 1:n){
    e0 <- sort(e[i,])
    e1[i] <- e0[alfa1]
    e2[i] <- e0[alfa2]
  }
  faixa <- range(r,e1,e2)
  par(pty="s")
  qqnorm(e1,axes=F,xlab="",type="l",ylab="",main="",ylim=faixa,lty=1)
  par(new=T)
  qqnorm(e2,axes=F,xlab="",type="l",ylab="",main="",ylim=faixa,lty=1)
  par(new=T)
  qqnorm(med,axes=F,xlab="",type="l",ylab="",main="",ylim=faixa,lty=3)
  par(new=T)
  dd <- qqnorm(r,xlab="Percentiles de la N(0,1)", ylab="Residuos",main="QQ Plot", ylim=faixa, cex=0.3, lwd=3)
  identify(dd$x,r,n=d, labels=nombres)
}


######## Influencia ###############################################################################################################
######## Construye gr�ficos de la Distancia de Cook para cada uno de los par�metros de localizaci�n en el modelo y un gr�fico de la
######## Distancia de Cook para la influencia general sobre el vector B. Los par�metros de la funci�n Influence.normal(objeto,a,b,d,nombres) son:
######## 1. Objeto. Objeto de R donde est�n guardados los resultados de la regresi�n
######## 2. a. N�mero de filas de gr�ficos
######## 3. b. N�mero de columnas de gr�ficos
######## 4. d. N�mero de observaciones que se quieren identificar en cada gr�fico.
######## 5. nombres. Nombre de la variable donde est�n los nombres o etiquetas de las observaciones. Si no existe tal etiqueta o no se quiere
######## usar, se debe diligenciar este par�metro como "".

Influence.normal <- function(objeto,a,b,d,nombres){
  y <- objeto$residuals + fitted(objeto)
  X <- model.matrix(objeto)
  if(length(nombres)<length(y)){
    nombres <- seq(1,length(y),by=1)}
  delta <- lm.influence(objeto)$coef
  DC <- diag(delta%*%solve(vcov(objeto))%*%t(delta))/ncol(X)
  maxy <- max(max(DC),3*mean(DC))
  plot(DC, main="Observaciones influyentes", xlab="�ndice", ylim=c(0,maxy), ylab="Distancia de Cook", cex=0.3, lwd=3)
  abline(3*mean(DC),0,lty=3)
  identify(DC, n=d, labels=nombres)
  p <- ncol(X)
  labels <- labels(coef(objeto))
  respuesta <- names(objeto$model[1])
  X11()
  par(mfrow=c(a,b))
  for(i in 1:p){
    a <- matrix(0,1,p)
    a[i] <- 1
    delta <- lm.influence(objeto)$coef[,i]
    DCi <- diag(delta%*%solve(a%*%vcov(objeto)%*%t(a))%*%t(delta))
    maxy <- max(max(DCi),3*mean(DCi))
    plot(DCi, main=labels[i], xlab="�ndice", ylim=c(0,maxy), ylab="Distancia de Cook", cex=0.3, lwd=3)
    abline(3*mean(DCi),0,lty=3)
    identify(DCi, n=d, labels=nombres)
  }
  DC
}



######################################
##################################
##############################################



library(zoo)
library(lmtest)
library(MASS)
library(readxl)

#####Lectura de datos ####################

datos_modelo <- read_excel("C:/Users/1018458579/Downloads/datos_recaudo.xlsx", sheet = "datos")

#####Modelos#############################

fit1<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$inflacion + datos_modelo$tasa_ocupacion + datos_modelo$DTF + datos_modelo$tasa_interv_br + datos_modelo$cambio_trm + datos_modelo$tasa_int_real + datos_modelo$var_anual_pib, data=datos_modelo)
fit2<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$inflacion + datos_modelo$tasa_ocupacion + datos_modelo$DTF + datos_modelo$tasa_interv_br + datos_modelo$cambio_trm + datos_modelo$var_anual_pib, data=datos_modelo)
fit3<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$inflacion + datos_modelo$tasa_ocupacion + datos_modelo$DTF + datos_modelo$tasa_interv_br + datos_modelo$cambio_trm, data=datos_modelo)
fit4<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$inflacion + datos_modelo$tasa_ocupacion + datos_modelo$DTF + datos_modelo$cambio_trm, data=datos_modelo)
fit5<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$inflacion + datos_modelo$tasa_ocupacion + datos_modelo$cambio_trm, data=datos_modelo)
fit6<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$tasa_ocupacion + datos_modelo$cambio_trm, data=datos_modelo)
fit7<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$tasa_ocupacion_7a + datos_modelo$cambio_trm, data=datos_modelo)

####Modelo Final######################
fit7<-lm(datos_modelo$recaudo_1000000000 ~ -1 + datos_modelo$IPVU_nom_medellin + datos_modelo$tasa_ocupacion_7a + datos_modelo$cambio_trm, data=datos_modelo)
summary(fit7)
AIC(fit7)
BIC(fit7)

####Correlaci�n de Pearson############
Correlaciones(fit7,3,2,1,"")

####Correlaciones parciales###########
Correlaciones.parcial(fit7,3,2,11,"")

####Validaci�n mejor modelo###########
ajuste.normal(fit7,3)
ajuste.normal(fit7,2)

####Puntos de alto leverage################
par(mfrow=c(1,1))
Leverage <- Leverage.normal(fit7,2,"")

####Puntos influencia######################
Influence.normal(fit7,2,2,2,"")

####Validaci�n supuesto normalidad#########
residuos <- Residuos.normal(fit7,2,"")
qqplot.normal(fit7,10000,0.001,1,"")

####Pron�stico#############################
fit7$fitted.values
write.table(fit7$fitted.values,"pron_7.csv",sep=',')


