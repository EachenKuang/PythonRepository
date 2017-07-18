# 一些小发现

## 2017.7.18
今天在研究gensim中的Corpora的时候，无意中发现了很多不知道的东西。

###
目的：因为之前语料库存储的是，每一行为一篇文章，而我需要获取每一小篇文章作为一个小语料库来预测它所属的主题类别，后来仔细研究bleiCorpora中的代码，终于让我发现了一些端倪。  

在bleiCorpora中，它有这样一个函数，它能够获取存储corpora中的位置之后的一行作为一个document，而我们无法简单获取它的offset
```python
def docbyoffset(self, offset):
    """
    Return the document stored at file position `offset`.
    """
    with utils.smart_open(self.fname) as f:
        f.seek(offset)
        return self.line2doc(f.readline())
```

而其中有个变量为index,它是ndarray类型，它保存了corpora每一行开头的位置。  
因此，配合bleiCorpora中的index，就能轻轻松松地读取每一行。  

```python
bow = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
bow.docbyoffset(bow.index[0]) #获取第一行
bow.docbyoffset(bow.index[1]) #获取第二行
```

这样就能轻轻松松地获得每一行

```python
print bow.length    # None
print bow.fname    #./timewindow_in3/corpus_2000-2001-2002.blei   
print bow.index    #一个ndarray数组
print bow.index.__len__()    #517 长度
print bow.id2word
print bow.__len__()    #517 长度
```




