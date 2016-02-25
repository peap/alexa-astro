Feature: Welcoming users to Pluto the Astronomer

  Scenario: LaunchRequest with new user
     Given our skill is enabled
      When a new user launches Pluto
      Then Alexa greets them and offers advice

  @wip
  Scenario: LaunchRequest with known user
     Given our skill is enabled
      When a known user launches Pluto
      Then Alexa tells them what's visible
