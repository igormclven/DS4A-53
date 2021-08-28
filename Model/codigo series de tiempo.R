library(fpp2)
library(readxl)

####Lectura de datos###########
serie_IPVU_tri <- read_excel("C:/Users/1018458579/Downloads/serie_ocupacion_ajuste_final.xlsx", sheet = "serie_IPVU_pronostico")
serie_Ocupacion_tri <- read_excel("C:/Users/1018458579/Downloads/serie_ocupacion_ajuste_final.xlsx", sheet = "serie_tasa_ocupacion_7a_pronost")


data_serie<-ts(serie_IPVU_tri$ipvu_medellin, frequency = 4, start = 1988)
data_serie<-ts(serie_Ocupacion_tri$ocupacion, frequency = 4, start = 1984)

###gráfico serie de tiempo

autoplot(data_serie)+
  labs(title = "Quarterly Tasa_ocupación_7a data series",
       x = "Timeline",
       y = "Tasa_ocupación_7a",
       colour = "blue")+
  theme_bw()
###descomposición

fit <- decompose(data_serie, type='additive')
fit <- decompose(data_serie, type= 'multiplicative')

###gráfico descomposición

autoplot(fit)+
  labs(title = "Time series decomposition",
       x = "Time",
       y = "Values",
       colour="Gears")+
  theme_bw()

###gráfico de serie de tiempo con su tendencia

autoplot(data_serie, series="Time series")+
  autolayer(trendcycle(fit), series="Trend")+
  labs(title = "Quarterly Tasa_ocupacion_7a data series",
       x = "Timeline",
       y = "Tasa_ocupacion_7a",
  )+
  theme_bw()

###gráfico de estacionalidad

ggseasonplot(data_serie)



###PRONOSTICO SEGÚN MÉTODOS


###naive
###no estacioSnalidad
###no tendencia, repite el ultimo dato

m1 <- naive(data_serie, h=8)
autoplot(m1)
autoplot(m1)+autolayer(fitted(m1), serie="Ajuste")
checkresiduals(m1)

###snaive
###estacionalidad
###no tendencia, repite el ultimo dato


m2 <- snaive(data_serie, h=8)
autoplot(m2)
autoplot(m2)+autolayer(fitted(m2), serie="Ajuste")
checkresiduals(m2)

###regresion
###estacionalidad
###tendencia

regresion <- tslm(data_serie ~ trend + season)
m3 <- forecast(regresion, h=8)
autoplot(m3)
autoplot(m3)+autolayer(fitted(m3), serie="Ajuste")
checkresiduals(m3)

###Método holt winters
###estacionalidad 'additive' o 'multiplicative'
###tendencia

m4 <- hw(data_serie, h=8, seasonal='multiplicative')
autoplot(m4)
autoplot(m4)+autolayer(fitted(m4), serie="Ajuste")
checkresiduals(m4)

###ARIMA
###estacionalidad 
###tendencia


modelo_arima <- auto.arima(data_serie)
m5 <- forecast(modelo_arima, h=4)
autoplot(m5)
autoplot(m5)+autolayer(fitted(m5), serie="Model fit")+
  labs(       x = "Timeline",
       y = "Tasa_ocupacion_7a",
  )
checkresiduals(m5)


###Red neuronal
###estacionalidad 
###no tendencia

neuronal_network <- nnetar(data_serie)
m6 <- forecast(neuronal_network, h=8)
autoplot(m6)
autoplot(m6)+autolayer(fitted(m6), serie="Ajuste")
checkresiduals(m6)


####mejor modelo

real <- c(2078.6397982,2114.0593283,2163.3934039,2158.7336392,2205.1706263, 2150.7458405,  2192.1666002,  2218.2349406,2234.7082582)
real <- c(58.5581425307401,59.5424127810841,60.1074247929903,60.4762789975062,57.1904201473565,44.925855710919,50.0972202425098,54.9670486432558)

data_real <- ts(real, frequency=4, start= 2019)

accuracy(m1,data_real)
accuracy(m2,data_real)
accuracy(m3,data_real)
accuracy(m4,data_real)
accuracy(m5,data_real)
accuracy(m6,data_real)


