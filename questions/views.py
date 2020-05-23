from django.shortcuts import render,redirect,get_object_or_404
from .models import Question,Quiz
from .forms import startquizzForm,sugestionForm,UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
# Create your views here.


def register(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'your account has been created! you are now readu to login !')
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html',{'form':form})




def home(request):
    form = startquizzForm()
    if request.method == 'POST':
        form = startquizzForm(request.POST,)
        if form.is_valid():
            number_of_word = form.cleaned_data['number_of_word']
            sounds = form.cleaned_data['sounds']
            number_of_gusses = form.cleaned_data['number_of_gusses']
            user=request.user.username
            if user == '' :
                quiz_username = 'Guest'
            else:
                quiz_username = user
            print(quiz_username)
            quiz = Quiz.objects.create(
                quiz_number_of_word = number_of_word,
                quiz_sounds = sounds,
                quiz_number_of_gusses = number_of_gusses,
                quiz_username = quiz_username,
            )
            quiz.save()
            print(number_of_word)
            print(sounds)
            print(number_of_gusses)
            allquestions=Question.objects.all()
            print(allquestions)
            y = 0
            for x in sounds:
                print(x) 
                sound = x
                for x in allquestions:
                    qst = x
                    if qst.vowel_name == sound:
                        quiz.quiz_questions.add(qst)
                        y = y+1
                        print("true")
                    else:
                        print("false")
            numofqst = y
            
            print("i am y")
            print(y)
            if number_of_word > numofqst :
                quiz.quiz_number_of_word = numofqst
                quiz.save()

            quiz.quiz_number_of_questions = quiz.quiz_number_of_word
            quiz.save()
            alnum = random.randint(1,int(y))
            print("this isssss ittt")
            print(alnum)
            cor = quiz.quiz_number_of_gusses
            print("ana llll cooor")
            print(cor)
            return redirect(getquestion,quiz=quiz,qst=alnum,cor=cor)                

    else:
        form = startquizzForm()
    return render(request ,'home.html',{'form':form})



def getquestion(request,quiz,qst,cor):
    form = sugestionForm()
    quiz = Quiz.objects.filter(pk = quiz).first()
    print(quiz)
    print(qst)
    print(qst == 1)
    allquest = quiz.quiz_questions.values()
    print(allquest)
    counteur = 1
    print(qst == counteur)
    for x in allquest:
        print(x)
        if counteur == qst:
            values_view = x.values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            print(first_value)
            question = Question.objects.filter(pk = first_value).first()
            print(question)
            print(counteur)
            print(qst)
            counteur= counteur+1
        else:
            counteur= counteur+1

    return render(request ,'question.html',{"quiz":quiz,"question":question,'form':form,"qst":qst,"cor":cor,})

def checkanswer(request):
    if request.method == 'POST':
        print('alolll')
        quiznum = request.POST.get('quiznum')
        print(quiznum)
        qstnum = request.POST.get('qstnum')
        print(qstnum)
        question = request.POST.get('question')
        print(question)
        vowel = request.POST.get('vowel')
        cor = request.POST.get('cor')
        print(vowel)
        youranswer=vowel
        theqst= Question.objects.filter(pk=question).first()
        thequiz= Quiz.objects.filter(pk=quiznum).first()
        correctanswer = theqst.vowel_name
        score = thequiz.quiz_score
        guesses = thequiz.quiz_number_of_gusses
        numword = thequiz.quiz_number_of_word
        if youranswer == correctanswer:
            if int(cor) == 0:
                score = score
            else:
                score = score + 1    
            print('correct')
            check = 'correct'
            numword = numword - 1
            thequiz.quiz_score = score
            thequiz.quiz_number_of_gusses = guesses 
            thequiz.quiz_number_of_word = numword
            thequiz.quiz_score_percentage = ((thequiz.quiz_score/thequiz.quiz_number_of_questions)*100)
            thequiz.save()    
            return render(request ,'resuiltquestion.html',{"quiz":thequiz,"qst":qstnum,"question":theqst,'check':check,"cor":cor})
        else:
            if int(cor) == 0:
                check = 'incorrect'
            else:    
                print('incorrect') 
                check = 'incorrect'
                cor = int(cor) - 1
            return redirect(getquestion,quiz=quiznum,qst=qstnum,cor=cor) 

        
    



def nextquestion(request):
    if request.method == 'POST':
        print('alolll next 2')
        quiznum = request.POST.get('quiznum')
        print(quiznum)
        qstnum = request.POST.get('qstnum')
        print(qstnum)
        qstid = request.POST.get('qstid')
        print(qstid)
        quiz = quiznum   
        thequiz = Quiz.objects.filter(pk=quiznum).first()
        oldtheqst= get_object_or_404(Question, id=qstid)
        thequiz.quiz_questions.remove(oldtheqst)
        thequiz.save()

        quqst = thequiz.quiz_number_of_current_question
        thequiz.quiz_number_of_current_question = quqst + 1
        thequiz.save()

        numword = thequiz.quiz_number_of_word
        alnum = random.randint(1,int(numword))
        print(quiz)
        cor = thequiz.quiz_number_of_gusses
    return redirect(getquestion,quiz=quiz,qst=alnum,cor=cor)  

@login_required
def profile(request):
    user_username=request.user.username 
    scores = Quiz.objects.filter(quiz_username = user_username)
    number_score = Quiz.objects.filter(quiz_username = user_username).count()
    print(user_username)
    print(scores)
    print(number_score)
    bestscore=0
    allscore=0
    for x in scores:
        quz = x
        print(quz)
        thequz= Quiz.objects.filter(id = quz.id).first()
        print(thequz)
        quzsco = thequz.quiz_score
        print(quzsco)
        allscore = allscore + quzsco
        if quzsco > bestscore :
            bestscore = quzsco
    return render(request ,'profile.html',{"number_score":number_score,"bestscore":bestscore,'allscore':allscore})  



def addqst(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfiles = request.FILES.getlist('myfile')
        print(myfiles)
        for x in myfiles:
            myfile = x
            print(x)
            model = myfile.name
            words = list(model) 
            print(words)
            i = 1
            for word in words:
                print(word)
                if i == 1:
                    wd = word
                    i=i+1 
                elif i == 2:
                    wd =wd + word
                    i=i+1
                elif i == 3:
                    wd =wd + word
                    i=i+1
                elif i == 4:
                    i=i+1
                elif i == 5:
                    i=i+1 
                elif i == 6:
                    i=i+1
                elif i == 7:
                    wd2 = word
                    i=i+1
                elif i == 8:
                    wd2 =wd2 + word
                    i=i+1
                else:
                    i=i+1

            print("wd")
            print(wd)
            print("wd2")
            print(wd2)

            if int(wd2) == 53:
                print("its 53")
                question = Question.objects.create(
                    word_name = "he",
                    word_sound = myfile ,
                    vowel_number = "01",
                    vowel_name = "i",
                )
                question.save()
                print(question.id)
            if int(wd2) == 54:
                print("its 54")
                question = Question.objects.create(
                    word_name = "hih",
                    word_sound = myfile ,
                    vowel_number = "02",
                    vowel_name = "I",
                )
                question.save()
                print(question.id)
            if int(wd2) == 55:
                print("its 55")
                question = Question.objects.create(
                    word_name = "hay",
                    word_sound = myfile ,
                    vowel_number = "03",
                    vowel_name = "e",
                )
                question.save()
                print(question.id)
            if int(wd2) == 57:
                print("its 57")
                question = Question.objects.create(
                    word_name = "heh",
                    word_sound = myfile ,
                    vowel_number = "04",
                    vowel_name = "ԑ",
                )
                question.save()
                print(question.id)
            if int(wd2) == 56:
                print("its 56")
                question = Question.objects.create(
                    word_name = "hah",
                    word_sound = myfile ,
                    vowel_number = "05",
                    vowel_name = "ᴂ",
                )
                question.save()
                print(question.id)
            if int(wd2) == 59:
                print("its 59")
                question = Question.objects.create(
                    word_name = "haw",
                    word_sound = myfile ,
                    vowel_number = "06",
                    vowel_name = "a",
                )
                question.save()
                print(question.id)
            if int(wd2) == 58:
                print("its 58")
                question = Question.objects.create(
                    word_name = "huh",
                    word_sound = myfile ,
                    vowel_number = "07",
                    vowel_name = "ᴧ",
                )
                question.save()
                print(question.id)
            if int(wd2) == 63:
                print("its 63")
                question = Question.objects.create(
                    word_name = "hoe",
                    word_sound = myfile ,
                    vowel_number = "08",
                    vowel_name = "o",
                )
                question.save()
                print(question.id)
            if int(wd2) == 60:
                print("its 60")
                question = Question.objects.create(
                    word_name = "hu",
                    word_sound = myfile ,
                    vowel_number = "09",
                    vowel_name = "ᶷ",
                )
                question.save()
                print(question.id)
            if int(wd2) == 61:
                print("its 61")
                question = Question.objects.create(
                    word_name = "who",
                    word_sound = myfile ,
                    vowel_number = "10",
                    vowel_name = "u",
                )
                question.save()
                print(question.id)                                                                                                
    qstindb = Question.objects.count()   
    return render(request, 'addqst.html',{"qstindb":qstindb,})