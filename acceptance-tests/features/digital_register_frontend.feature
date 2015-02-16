Feature: Digital Register


#US024 Property Owner in the summary box DigitalRegistry
#Acceptance Criteria
  #  No private individuals are displayed in the owner summary box
  #  This is being weaseled around by only popping the database with
  #  non private individuals.

@US024 @Single_Owner @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by an individual
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
  #*************************************************************


@US024 @Multiple_Owner @DigitalRegistry
Given I am a citizen
And I have a property
And the property is owned by an individual
And the property is co owned by another individual
When I view the property detail page
Then I can see all the owners the property


@US033  @ViewFullAddress @DigitalRegistry
Given I am a citizen
And I have logged in
And I have a property
When I view the property detail page
Then I see the full address of the property
