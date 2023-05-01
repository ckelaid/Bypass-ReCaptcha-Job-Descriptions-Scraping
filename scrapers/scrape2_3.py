
import importlib
import deps as dep
import driver_config as dc
importlib.reload(dep)
importlib.reload(dc)

dep.warnings.filterwarnings("ignore") # ignore the deprecation warnings

#browser = d.initialize_driver()
def human_like_mouse(action:dep.ActionChains, startElem):
    # B-spline function
    # Curve base:
    points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
    points = dep.np.array(points)

    x = points[:,0]
    y = points[:,1]


    t = range(len(points))
    ipl_t = dep.np.linspace(0.0, len(points) - 1, 100)

    x_tup = dep.si.splrep(t, x, k=3)
    y_tup = dep.si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = dep.si.splev(ipl_t, x_list) # x interpolate values
    y_i = dep.si.splev(ipl_t, y_list) # y interpolate values

    
    start_element = startElem

    action.move_to_element(start_element)
    action.perform()

    c = 5
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y)
        action.perform()
        #print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))   
        i += 1    
        if i == c:
            break


def get_num_pages(url:str) -> int:

    browser = dc.initialize_driver()
    t = dep.random.randint(8,10)
    dep.WebDriverWait(browser, t)
    browser.get(url)
    
    try:
        dep.WebDriverWait(browser, 20).until(
                dep.EC.presence_of_element_located((dep.By.CLASS_NAME, 'text-nowrap'))
            )
        max_jobs = browser.find_element(dep.By.CLASS_NAME, 'text-nowrap').text.split(' ')[5]
        max_jobs = int("".join(max_jobs.split(','))) # remove ',' so that we can convert to int 
        num_pages = dep.math.ceil(max_jobs/100) # /100 because we iterate 100 links per page
        browser.quit()
    
    except Exception:
        # Check that exception is b/c of Captcha
        if browser.find_elements(dep.By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):
            bypassCaptcha1(browser)

             # Check if we get second captcha check
            if browser.find_elements(dep.By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):
                
                bypassCaptcha2(browser)
                dep.time.sleep(10)

        dep.time.sleep(5)
        max_jobs = browser.find_element(dep.By.CLASS_NAME, 'text-nowrap').text.split(' ')[5]
        max_jobs = int("".join(max_jobs.split(','))) # remove ',' so that we can convert to int 
        num_pages = dep.math.ceil(max_jobs/100) # /100 because we iterate 100 links per page
        browser.quit()

    return num_pages


def bypassCaptcha1(browser):

    # Switch to captcha iframe
    iframe = browser.find_elements(dep.By.TAG_NAME,'iframe')[0]
    browser.switch_to.frame(iframe)
    iframe = browser.find_elements(dep.By.TAG_NAME,'iframe')[0]
    browser.switch_to.frame(iframe)
    
    # Captcha check button
    captcha_check = dep.WebDriverWait(browser, 10).until(dep.EC.element_to_be_clickable((dep.By.XPATH, "//*[@id='recaptcha-anchor']")))
    browser.implicitly_wait(12)
    action =  dep.ActionChains(browser)
    # Simulate human like mouse movements
    human_like_mouse(action, captcha_check)
    captcha_check.click() # Click captcha check


    browser.implicitly_wait(8)
    action =  dep.ActionChains(browser)
    human_like_mouse(action, captcha_check)

    browser.switch_to.default_content()

    print('\nSuccessfuly bypassed Captcha 1!\n')

# Check if we get second captcha check
#  if browser.find_elements(By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):

def bypassCaptcha2(browser):

    t = dep.random.randint(8,10)
    browser.implicitly_wait(t)

    iframe2 = browser.find_elements(dep.By.TAG_NAME,"iframe")[0]
    browser.switch_to.frame(iframe2)
    iframe3 = browser.find_elements(dep.By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")[0]
    browser.switch_to.frame(iframe3)
    # Find nearest element to #shadow-root (closed)
    elem = browser.find_element(dep.By.XPATH, '//div[@class="button-holder help-button-holder"]')
    browser.implicitly_wait(10)
    elem.click() # click on it
    browser.switch_to.default_content()

    print('\nSuccessfuly bypassed Captcha 2!\n')  


def get_job_links(x:str) -> list:

    #x = input('\nPlease enter a keyword: \n\n')
    base = 'https://www.higheredjobs.com/search/advanced_action.cfm?Remote=&Keyword='
    page_num = 1
    page = '&PosType=&InstType=&JobCat=&Region=0&SubRegions=&Metros=&OnlyTitle=0&JobCatType=&StartRow='+str(page_num)+'&SortBy=1&NumJobs=100&CatType='

    url = base+x+page

    print(url)

    num_pages = get_num_pages(url)

    page_links = []
    page_links.append(url) #1st page

    # for page 2 until the last page
    for p in range(1, num_pages): #=> we want to +100 for as many pages as we iterate through to the page link, starting at the 2nd page
        page_num = page_num + 100
        page = '&PosType=&InstType=&JobCat=&Region=0&SubRegions=&Metros=&OnlyTitle=0&JobCatType=&StartRow='+str(page_num)+'&SortBy=1&NumJobs=100&CatType='
        url = base+x+page
        page_links.append(url)

    print("There are {} pages".format(len(page_links)))
    # Save page links
    with open('Page_Links.pkl', 'wb') as f:
                dep.pickle.dump(page_links, f)
    #print("\nDiscerning jobs relating to 'workday'\n")
    # 5 min
    job_links = []

    for link in page_links:
        t = dep.random.randint(8,10)
        dep.time.sleep(t)
        browser = dc.initialize_driver()
        browser.get(link)
        try:
            # wait for page to load
            dep.WebDriverWait(browser, 20).until(
                dep.EC.presence_of_element_located((dep.By.CLASS_NAME, 'col-sm-7'))
            )
            # get job links
            div = browser.find_elements(dep.By.CLASS_NAME, 'col-sm-7')
            for d in div:
                job_links.append(d.find_element(dep.By.CSS_SELECTOR, 'a').get_attribute('href'))
            browser.quit()
            with open('JOB_links.pkl', 'wb') as f:
                dep.pickle.dump(job_links, f)
        except Exception:
            # Check that exception is b/c of Captcha
            if browser.find_elements(dep.By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):

                #bypassFullCaptcha()
                bypassCaptcha1(browser)
                
                # Check if we get second captcha check
                if browser.find_elements(dep.By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):
                    
                    bypassCaptcha2(browser)
                    dep.time.sleep(10)

            try:
                print('Looking for job link\n')
                    
                # Successfully moved out of Captcha

                # wait for page to load
                dep.WebDriverWait(browser, 20).until(
                        dep.EC.presence_of_element_located((dep.By.CLASS_NAME, 'col-sm-7'))
                ) 
                # get job links
                div = browser.find_elements(dep.By.CLASS_NAME, 'col-sm-7')
                for d in div:
                    job_links.append(d.find_element(dep.By.CSS_SELECTOR, 'a').get_attribute('href'))
                browser.quit()
                with open('JOB_links.pkl', 'wb') as f:
                    dep.pickle.dump(job_links, f)
            
            except Exception:
                # API limit exceeded and need to wait, pause 20 minutes and try again
                
                browser.quit()
                print('Pausing 30 minutes, buster API overused!')
                dep.time.sleep(1800) # wait 30 minutes :( looooooong

                browser = dc.initialize_driver()
                browser.get(link)

                bypassCaptcha1(browser)

                bypassCaptcha2(browser)
                dep.time.sleep(10)

                print('Looking for job link\n')
                    
                # Successfully moved out of Captcha

                # wait for page to load
                dep.WebDriverWait(browser, 20).until(
                        dep.EC.presence_of_element_located((dep.By.CLASS_NAME, 'col-sm-7'))
                ) 
                # get job links
                div = browser.find_elements(dep.By.CLASS_NAME, 'col-sm-7')
                for d in div:
                    job_links.append(d.find_element(dep.By.CSS_SELECTOR, 'a').get_attribute('href'))
                browser.quit()
                with open('JOB_links.pkl', 'wb') as f:
                    dep.pickle.dump(job_links, f)
    
    
    # Deleting wrong entries
    del_ix = []
    for i in range(len(job_links)):
        if job_links[i] == 'javascript:;':
            del_ix.append(i) 

    # Also check that no job_links == category_page url
    for j in range(len(job_links)):
        if job_links[j] == 'https://www.higheredjobs.com/search/advanced_action.cfm?Remote=&Keyword='+x+'&PosType=&InstType=&JobCat=&Region=0&SubRegions=&Metros=&OnlyTitle=0&JobCatType=&SortBy=1&StartRow=1':
            del_ix.append(j)

    if len(del_ix) > 0:
        # delete 'javascript:;' entries & incorrect url entries
        del job_links[del_ix[0]]

        drop = 1
        for i in range(1, len(del_ix)):
            del job_links[del_ix[i]-drop]
            drop = drop + 1
    
    print("There are {} jobs to scrape".format(len(job_links)))

    # Save job links
    with open('Job_Links.pkl', 'wb') as f:
                dep.pickle.dump(job_links, f)

    return job_links[:15]
    

def scrape_job_info(job_links:list) -> dict:

    # 45 minutes => for 100 jobs
    job_attrs = []
    job_dict = {}
    not_scraped = 0
    scraped = 0
    smile = 0

    for link in job_links: #start at job 2501, bc job 1 is index 0
        browser = dc.initialize_driver()
        t = random.randint(8,10)
        WebDriverWait(browser, t)
        browser.get(link) # for 1st job

        try:
            del_div = browser.find_elements(By.CLASS_NAME, 'row')
            # Check if post has been deleted
            if del_div[6].text != 'We require users to verify the reCaptcha below to view deleted positions.\nRelated Searches:\nBusiness and Financial Services\nCreate your free job search account\nReceive new jobs by email\nPost your resume/CV\nTrack your applications\nJoin Now\nHave an account? Sign in':

                job_title = browser.find_element(By.ID, 'jobtitle-header').text
                job_loc = browser.find_element(By.CLASS_NAME, 'job-loc').text
                div = browser.find_elements(By.ID, 'jobAttrib')
                job_attr = div[0].find_element(By.CLASS_NAME, 'job-info').text.split('\n') # get job data
                        #job_attr = [job_title] + job_attr
                div = browser.find_elements(By.ID, 'job')
                job_desc = div[0].find_element(By.ID, 'jobDesc').text#.split('\n')
                    #job_attr.append(job_desc)
                    #job_attrs.append(job_attr)
                
            #else: # if post is delete
                job_attr = [job_title] + [job_loc] + job_attr # puts title at the begining of the list
                job_attr.append(job_desc) # Append job_description
                job_attrs.append(job_attr) # Append job details as list inside another list 
                
                scraped = scraped + 1

            elif IndexError:
                not_scraped = not_scraped + 1

                    #browser.quit()
        except NoSuchElementException: # If cannot find element
            #job_title = browser.find_element(By.ID, 'VIPTitle').text
            #div = browser.find_element(By.ID, 'mainContent').text
            #job_desc = div[len(job_title)+1:] # Get rid of Job title in job description
            #job_attr = ['n/a','n/a','n/a','n/a','n/a']
            not_scraped = not_scraped + 1
        
        #except IndexError:
            #not_scraped = not_scraped + 1

                        
            #job_attr = [job_title] + job_attr # puts title at the begining of the list
            #job_attr.append(job_desc) # Append job_description
            #job_attrs.append(job_attr) # Append job details as list inside anothe list
        browser.quit()
        smile = smile +1
        if smile == 1:
            print('\nScraping away...\n')
            print('0  0\n')
            print('\__/\n')
        if smile % 100 == 0:
            print("{} jobs have been scraped so far...\n".format(scraped))
            print('0  0\n')
            print('\__/\n')
        
        # Save progress
        if smile % 500 == 0: # Every 500 jobs save as pickle
            # Store data (serialize)
            with open('Job_Attrs_'+str(smile)+'.pkl', 'wb') as f:
                pickle.dump(job_attrs, f)

            #load pickle lists => need to concatenate them all then store them in dict
            #with open('file_name.pkl', 'rb') as f:
                #mynewlist = pickle.load(f)
    
    if not_scraped > 0:

        if not_scraped == 1:
            print('Unfortunately, information for {} job was unable to be scraped.'.format(not_scraped))
        
        elif not_scraped > 1:
            print('Unfortunately, information for {} jobs was unable to be scraped.'.format(not_scraped))

    print("\nInformation on a total of {} jobs has been scraped\n".format(scraped))

    # Store in dictionary
    for i in range(len(job_attrs)):
        job_dict['Job ' + str(i+1)] = job_attrs[i]

    return job_dict



def fix_dict_lens(job_dict:dict) -> dict:

    ix = 0
    # Get dictionary lengths
    dic_lens = []
    for val in job_dict.values():
        dic_lens.append(len(val))
    
    # Making all dictionary entries lengths equal
    for i in range(len(dic_lens)):

        if dic_lens[i] == 6: # If Salary & Application Due are missing

            # The corresponding job in dicitonary
            job_dict['Job '+str(i+1)].insert(3, 'n/a') # Insert 'n/a' for Salary
            job_dict['Job '+str(i+1)].insert(5, 'n/a') # Insert 'n/a' for App. due
        
        if dic_lens[i] == 7: # If Salary or Application Due is missing

            if job_dict['Job '+str(i+1)][3].startswith('Salary'): # if salary is present
                # Insert 'n/a' for App. due
                job_dict['Job '+str(i+1)].insert(5, 'n/a')
            elif job_dict['Job '+str(i+1)][4].startswith('Application'): # else if App. Due is present (index 4 for length 7)
                # Insert 'n/a' for Salary
                job_dict['Job '+str(i+1)].insert(3, 'n/a')
            elif job_dict['Job '+str(i+1)][5].startswith('Announcement'): # In case of 'Annoucement' entry
                job_dict['Job '+str(i+1)].insert(3, 'n/a') # Insert 'n/a' for Salary
                job_dict['Job '+str(i+1)].insert(5, 'n/a') # Insert 'n/a' for App. due
                
                # get rid of 'Announcement' entry, which is 2 indexes more than before since we inserted n/a's
                del job_dict['Job '+str(i+1)][7]

        if dic_lens[i] == 9: # if all entries are full but we also have the 'Announcement', then simply remove that one
            if job_dict['Job '+str(i+1)][7].startswith('Announcement'):
                del job_dict['Job '+str(i+1)][7]

    return job_dict



# Save results
def save_csv(keyword:str, job_dict:dict) :

    df = pd.DataFrame(job_dict).T.rename(columns={0:'Title',1:'Location',2:'Type',3:'Salary',4:'Posted On',5:'Due',6:'Category',7:'Description'})
    
    df.to_csv(keyword + '_Jobs.csv', index=False)



def get_job_info(keyword:str) -> dict:

    job_links = get_job_links(keyword)

    print(len(job_links))

    print('\nBeginning the scraping journey... \n\n')

    job_dict = scrape_job_info(job_links)

    print('Dictionary length is {}'.format(len(job_dict.values())))

    return job_dict


if __name__ == '__main__':

    x = input('\nPlease enter a keyword: \n\n')

    save_csv(x, fix_dict_lens(get_job_info(x)))

    print('\nGrabbing salary infromation from description\n')

    print('\nThis will take between 20 and 30 minutes, so sit back and relax\n')

    dep.GetSalary.grab_salary_from_desc(x+'_Jobs.csv')

    print('\nDONE\n')

    print('\nThe scraping journey has ended.\n')
    print("Your results are found in your current directory in the file: "+x+"_Jobs_Updated.csv\n")

