Feature: US024 Property Owner in the summary box

@US024 @One_Individual @DigitalRegistry
Scenario: find a single property owner
Given I am a citizen
And I have a property owned by an individual
When I view the property detail page
Then I can see who owns the property


@US024 @Multiple_Owners @DigitalRegistry
Scenario: find multiple property owners
Given I am a citizen
And I have a property owned by a multiple individuals
When I view the property detail page
Then I can see all the owners the property
