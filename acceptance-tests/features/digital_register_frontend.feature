Feature: Digital Register


#US024 Property Owner in the summary box DigitalRegistry
#Acceptance Criteria
  #  No private individuals are displayed in the owner summary box

@US024 @Non_Private_Individual @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by a non-private individual
When I view the property detail page
Then I can see who owns the property

  #********************** UNIT TEST*****************************
  # Non-Private Individual classes include
  #	Public Limited Company
  #	Housing Association
  #	Local Authority
  #	County Council
  #	Charity
  #	Overseas Company
  #*****************************************************************

@US024 @Private_Individual @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by a private individual
When I view the property detail page
Then I cannot see who owns the property

@US024 @Multiple_Non_Private_Individual @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by a non private individual
And the property is co owned by another non private individual
When I view the property detail page
Then I can see all the owners the property

@US024 @Multiple_Private_Individual @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by a private individual
And the property is co owned by another private individual
When I view the property detail page
Then I cannot see who owns the property

@US024 @Mixed_Owners @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by a non private individual
And the property is co owned by another private individual
When I view the property detail page
Then I 	1) can see all the owners the property - hope not
  2) can see just the non-pi and an indication that there is another owner - maybe
  3) cannot see who owns the property



#US033  View full address in summary box in digital register
#Acceptance Criteria
 # Be able to display the full address - (for the show and tell)
 # The address must be in the same format as when displayed on the Gov.UK Property Pages
 # If the information relating to the address is not available then a meaningful message must    be displayed

@US033  @ViewFullAddress @DigitalRegistry
Given I am a citizen
And I have logged in
And I have a property
When I view the property detail page
Then I see the full address of the property
