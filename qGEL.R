library(easypackages)
suppressWarnings(
  libraries("dplyr","Rcpp","RcppArmadillo","RcppEigen","parallel",
            "RSpectra","pryr","tidyr","data.table","Matrix")
)

# Creating weighted marginal

freqTables <- function(x){
  v <- table(x)/length(x)
  w <- data.frame(t(as.numeric(v)))
  names(w) <- names(v)
  return (w)
}
fbyEachClass <- function(r_, f_, d_){

  if(is.null(dim(r_))){
    Q <- matrix(1, nrow = (ncol(d_)-1), ncol = 1)
  }
  else {
    binary_row_weights_ <- as.matrix(rbindlist(
      lapply(1:nrow(r_), function(i) freqTables(r_[i,])), fill = T))
    binary_row_weights_[is.na(binary_row_weights_)] <- 0
    binary_row_weights <- as.data.frame(binary_row_weights_)
    R <- binary_row_weights[sort(names(binary_row_weights))]

    binary_f_weights_ <- as.matrix(rbindlist(
      lapply(1:ncol(f_), function(i) freqTables(f_[,i])), fill = T))
    binary_f_weights_[is.na(binary_f_weights_)] <- 0
    binary_f_weights <- as.data.frame(binary_f_weights_)
    `F` <- binary_f_weights[sort(names(binary_f_weights))]

    Q <- eigenMapMatMult(as.matrix(`F`), as.matrix(t(R)))
  }
  return(Q/max(Q))
}

# #diagonal aspects

getD <- function(i, d_, dis_){
  fbyEachClass(r_ = sapply(d_[dis_[[i]],]  %>%
                             select(-Class), as.character),
               f_ = sapply(d_[dis_[[i]],]  %>%
                             select(-Class), as.character),
               d_ = d_)
}


qgel <- function(source.data_, k = 10, class_var = NULL, 
                     learning_method = 'unsupervised'){


  if (learning_method == "supervised"){
    source.data_ <- dplyr::rename_(source.data_, Class = class_var)
    source.data_$Class <- factor(x = source.data_$Class,
                                 names(sort(table(source.data_$Class),
                                            decreasing = T)))

    source.data <- as.data.frame(apply(source.data_ %>%
                                         arrange(Class), 2, as.character))
    W_ <- source.data
  }
  else{
    W_ <- source.data_
  }


  if (learning_method == "supervised"){

    class_combs <- as.data.frame.matrix(
      t(
        combn(x = unique(W_$Class), m = 2)))
    names(class_combs) <- c('c_i', 'c_j')

    
    if(n_distinct(W_$Class) == 2){
      diag_index_sets <- lapply(1:2, function(i)
        rownames(W_[which(W_$Class == unique(W_$Class)[i]),]))
    }
    else{
      diag_index_sets <- lapply(1:n_distinct(W_$Class), function(i)
        rownames(W_[which(W_$Class == unique(W_$Class)[i]),]))
    }

    D <- lapply(1:length(diag_index_sets), function(i)
      getD(i, d_ = W_, dis_ = diag_index_sets))
    names(D) <- unique(W_$Class)
    
    b <- bdiag(D) %>% as.matrix()
    
    S <- eigenMapMatMult(b,
                         as.matrix(sapply(W_ %>%
                                            select(-Class),
                                          function(x)
                                            as.numeric(as.character(x)))))
  }
    
  else {
    u <- fbyEachClass(r_ = sapply(W_, as.character),
                      f_ = sapply(W_, as.character),
                      d_ = W_)

    S <- eigenMapMatMult(u,
                         as.matrix(sapply(W_ ,
                                          function(x)
                                            as.numeric(as.character(x)))))

  }

  if(k == 'max' | k >= nrow(W_)){
    k <- nrow(W_)
  }
  else{
    k <- k
  }

  V <- svd(S, nv = k)$v

  ret <- list()
  ret$V <- V
  ret$W_ <- W_

  if (learning_method == "supervised"){
    ret$embed <- as.data.frame(
      as.matrix(
        sapply(
          W_ %>%
            select(-Class), function(x) as.numeric(as.character(x)))) %*% V)
    ret$embed[class_var] <- source.data$Class
  }
  else{
    ret$embed <- as.data.frame(
      as.matrix(
        sapply(
          W_, function(x) as.numeric(as.character(x)))) %*% V)
  }

  return(ret)}
