{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Te damos la bienvenida a Colaboratory",
      "provenance": [],
      "collapsed_sections": [],
      "toc_visible": true,
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/luiscaballeroramos/DeCoder/blob/EC3_1_8_DesignOfJoints/DeCoder.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "5JPVNXqMLRPZ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class TOC():\n",
        "  def __init__(self,refidRegex,refsepRegex,refsep,namRegex,sepRegex,numRegex):\n",
        "    self.refidRegex=refidRegex\n",
        "    self.refsepRegex=refsepRegex\n",
        "    self.refsep=refsep\n",
        "    self.refRegex=refidRegex+'(?:'+refsepRegex+'{1}'+refidRegex+'+)+'\n",
        "    self.namRegex=namRegex\n",
        "    self.sepRegex=sepRegex\n",
        "    self.numRegex=numRegex\n",
        "    self.tocRegex=self.refRegex+'\\s*'+namRegex+'\\s*'+sepRegex+'\\s*'+numRegex\n",
        "    self.tocList=[]\n",
        "    pass\n",
        "  def addToc(self,toc):\n",
        "    if len(list(x for x in self.tocList if x.ref == toc.ref)) == 0:\n",
        "      self.tocList.append(toc)\n",
        "      pass\n",
        "    pass\n",
        "  def printTOC(self,num=None):\n",
        "    table=[]\n",
        "    if num is None:\n",
        "      for toc in TOC_EC3.tocList:\n",
        "        table.append([toc.ref,toc.name,toc.begin.page,toc.level])\n",
        "        pass\n",
        "    else:\n",
        "      toc=TOC_EC3.tocList[num]\n",
        "      table.append([toc.ref,toc.name,toc.begin.page,toc.level])\n",
        "      pass\n",
        "    print(tabulate(table,headers=['Ref.','Name','Begin page','Level'], tablefmt='orgtbl'))\n",
        "    pass\n",
        "  pass\n",
        "\n",
        "class PDFlocation():\n",
        "  def __init__(self,page,begin=None,end=None):\n",
        "    self.page=page\n",
        "    if begin is None:\n",
        "      self.begin=None\n",
        "      self.end =None\n",
        "    else:\n",
        "      self.begin=int(begin)\n",
        "      if end is None:\n",
        "        self.end=int(begin)\n",
        "      else:\n",
        "        self.end=end\n",
        "        pass\n",
        "      pass\n",
        "    pass\n",
        "  pass\n",
        "\n",
        "class toc():\n",
        "  def __init__(self,ref,refsep,name,begin=None,end=None,level=None):\n",
        "    self.ref=join(list(filter(lambda item: item, re.split('\\.*',ref))),refsep)\n",
        "    self.name=name\n",
        "    self.begin=begin\n",
        "    self.end=end\n",
        "    self.setLevel()\n",
        "    pass\n",
        "  def setLevel(self):\n",
        "    self.level = len(list(filter(lambda item: item, re.split('\\.*',self.ref))))-1\n",
        "    pass\n",
        "  pass\n",
        "\n",
        "def Luis():\n",
        "  print('Luis Luis')"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}