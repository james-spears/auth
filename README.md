# Site
This is a web application.

## Plan

Entities

- User
  - (method) addPermission
  - (method) listPermissions
  - (method) getPermission
  - (method) removePermission

- Team
  - (method) addUser
  - (method) listUsers
  - (method) getUser
  - (method) removeUser

- Permission
  - (property) name
  - (property) description

  - (method) getName
  - (method) updateName

  - (method) getDescription
  - (method) updateDescription

- Release
  - (method) addProject
  - (method) listProjects
  - (method) getProject
  - (method) removeProject

- Gate
  - (method) addCondition
  - (method) listConditions
  - (method) getCondition
  - (method) removeCondition

- Condition
  - (property) name
  - (property) description

  - (method) getName
  - (method) updateName

  - (method) getDescription
  - (method) updateDescription

- Project
  - (method) addGate
  - (method) listGates
  - (method) getGate
  - (method) removeGate

- Scope
  - (method) addRequirement
  - (method) listRequirements
  - (method) getRequirement
  - (method) removeRequirement

- Requirement
  - (property) name
  - (property) description

  - (method) getName
  - (method) updateName

  - (method) getDescription
  - (method) updateDescription

- Asset
  - (property) name
  - (property) description
  
  - (method) getName
  - (method) updateName

  - (method) getDescription
  - (method) updateDescription

- Artifact
  - (method) addAsset
  - (method) listAssets
  - (method) getAsset
  - (method) removeAsset

- Inspection
  - (property) name
  - (property) description

  - (method) getName
  - (method) updateName

  - (method) getDescription
  - (method) updateDescription