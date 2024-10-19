from bs4 import BeautifulSoup

# Example HTML content
html_content = """
<html>
<body>

<div id='main'>
    <p id='a'>Hi</p>
    <p id='b'>Gola</p>
    <div id='ab'>
        <p id="aba">
            <p id="g"></p>
        </p>
        <p id="abb">2</p>
        <p id="abc">3</p>
    </div>
    <p id ="c">Diya</p>
    <div><p id='fir'>fir</p></div>
    <p id ="d">Raksha</p>
</div>

</body>
</html>
"""

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")   #holds 'document' as current tag -->child:html tag  name:document

# print(list(soup.descendants),list(soup.children))
# p_tag = soup.find(name='p',attrs={'id':'a'},string='HI')
# p_tag = soup.find_all(name='p',attrs={'id':'a'},string='HI')

# p_tag = soup.find('p').find_all_next('p')  #down.find_all() aftert current tag ,never looks up to current tag ,{{{it doesnt skip tags inside current tag -->combination of current.find_all()+ down.find_all() applied to after current tag}}} 
# p_tag = soup.find('p').find_next('p')    #cdown.find() aftert current tag ,never looks up to current tag
# p_tag = soup.find('p').find_all_prev('p')  # up.find_all() behind current tag ,never looks down to current tag
# p_tag = soup.find('p').find_pre('p')  # up.find()  behind current tag ,never looks down to current tag

# p_tag = soup.find('div',{'id':'ab'}).find_previous_siblings()
# p_tag = soup.find('div',{'id':'ab'}).find_previous_sibling()
# p_tag = soup.find('div',{'id':'ab'}).find_next_sibling('p',{'id':'d'})
p_tag = soup.find('div',{'id':'ab'}).find_next_siblings()

print(p_tag)
