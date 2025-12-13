grammar CML;

/*
 * Context Mapper DSL (CML) Grammar for ANTLR4
 */

// --- Parser Rules ---

definitions
    : (imports | topLevel)* EOF
    ;

imports
    : 'import' STRING
    ;

topLevel
    : contextMap
    | boundedContext
    | domain
    | useCase
    | stakeholderSection
    | valueRegister
    | userStory
    ;

// --- Strategic DDD ---

contextMap
    : 'ContextMap' name? '{'
      contextMapSetting*
      relationship*
      '}'
    ;

contextMapSetting
    : 'type' '='? contextMapType
    | 'state' '='? contextMapState
    | 'contains' idList
    | 'realizes' idList
    ;

contextMapType
    : 'SYSTEM_LANDSCAPE' | 'ORGANIZATIONAL'
    ;

contextMapState
    : 'AS_IS' | 'TO_BE'
    ;

relationship
    : relationshipEndpoint relationshipConnection relationshipEndpoint (':' ID)? ('{' relationshipAttribute* '}')?
    ;

relationshipConnection
    : relationshipArrow | relationshipKeyword
    ;

relationshipEndpoint
    : relationshipRoles? name relationshipRoles?
    ;

relationshipKeyword
    : 'Customer-Supplier' | 'Upstream-Downstream' | 'Downstream-Upstream' | 'Partnership' | 'Shared-Kernel'
    ;

relationshipRoles
    : '[' relationshipRole (',' relationshipRole)* ']'
    ;

relationshipRole
    : 'ACL' | 'CF' | 'OHS' | 'PL' | 'SK' | 'U' | 'D' | 'S' | 'C' | 'P'
    ;

relationshipArrow
    : '<->' | '<-' | '->'
    ;

relationshipAttribute
    : 'implementationTechnology' '='? STRING
    | 'downstreamRights' '='? downstreamRights
    | 'exposedAggregates' '='? idList
    ;

downstreamRights
    : 'VETO_RIGHT' | 'INFLUENCER'
    ;

boundedContext
    : 'BoundedContext' name ('implements' idList)? ('realizes' idList)? body=contentBlock?
    ;

boundedContextAttribute
    : 'type' '='? boundedContextType
    | 'domainVisionStatement' '='? STRING
    | 'implementationTechnology' '='? STRING
    | 'responsibilities' '='? STRING
    | 'knowledgeLevel' '='? knowledgeLevel
    | 'realizes' '='? idList
    ;

boundedContextType
    : 'FEATURE' | 'SYSTEM' | 'APPLICATION' | 'TEAM'
    ;

knowledgeLevel
    : 'CONCRETE' | 'ABSTRACT'
    ;

domain
    : 'Domain' name body=contentBlock?
    ;

subdomain
    : 'Subdomain' name ('type' subdomainType)? body=contentBlock?
    ;

subdomainType
    : 'CORE_DOMAIN' | 'SUPPORTING_DOMAIN' | 'GENERIC_SUBDOMAIN'
    ;

module
    : 'Module' name body=contentBlock?
    ;

// --- Tactic DDD (Sculptor) ---

aggregate
    : 'Aggregate' name body=contentBlock?
    ;

domainObject
    : STRING? simpleDomainObjectOrEnum
    ;

simpleDomainObjectOrEnum
    : simpleDomainObject | enumDecl
    ;

simpleDomainObject
    : entity | valueObject | domainEvent | commandEvent | dataTransferObject
    ;

entity
    : 'abstract'? 'Entity' name ('extends' '@'? name)? body=entityBody?
    ;

entityBody
    : '{'
      'aggregateRoot'?
      feature*
      '}'
    ;

valueObject
    : 'abstract'? 'ValueObject' name ('extends' '@'? name)? body=valueObjectBody?
    ;

valueObjectBody
    : '{'
      feature*
      '}'
    ;

domainEvent
    : 'abstract'? 'DomainEvent' name ('extends' '@'? name)? body=domainEventBody?
    ;

domainEventBody
    : '{'
      'aggregateRoot'?
      'persistent'?
      feature*
      '}'
    ;

commandEvent
    : 'abstract'? 'CommandEvent' name ('extends' '@'? name)? body=commandEventBody?
    ;

commandEventBody
    : '{'
      feature*
      '}'
    ;

dataTransferObject
    : 'DataTransferObject' name ('extends' '@'? name)? body=dtoBody?
    ;

dtoBody
    : '{'
      feature*
      '}'
    ;

enumDecl
    : 'enum' name '{'
      'aggregateLifecycle'?
      idList
      ';'?
      '}'
    ;

// Tactical DDD Features - The core fix for attribute parsing
feature
    : repository
    | operation
    | attribute
    // Fallback to swallow unrecognized statements inside DDD blocks
    | rawStatement
    ;

// Explicit attribute rule to avoid ambiguity
attribute
    : visibility? reference='-'? type name 'key'? ';'?
    ;

// Operation rule - allow missing parentheses and trailing hints
operation
    : visibility? ('def' | '*')? returnType=type? name
      '(' parameterList? ')'
      operationHint?
      operationTail?
      ('throws' idList)?
      ';'?
    ;

operationHint
    : ':' operationHintType stateTransition?
    ;

operationHintType
    : 'read-only' | 'read' | 'write'
    ;

operationTail
    : ('publish' | 'subscribe') 'to' (~(';' | '}'))+
    ;

// Fallback for complex operations that don't match standard signature
// This replaces RawFeature but is more constrained
// We'll rely on the specific operation rule first

contentBlock
    : '{' contentEntry* '}'
    ;

contentEntry
    : contentItem
    | feature
    ;

subdomainAttribute
    : 'type' '='? subdomainType
    | 'domainVisionStatement' '='? STRING
    ;

contentItem
    : contentBlock
    | aggregate
    | domainObject
    | service
    | repository
    | boundedContextAttribute
    | subdomainAttribute
    | setting
    | useCase
    | subdomain
    | module
    | application
    | contextMap
    | domain
    | ownerDecl
    ;

ownerDecl
    : 'owner' '='? name ';'?
    ;

setting
    : 'basePackage' '=' qualifiedName ';'?
    ;

parameter
    : '@'? type name
    ;

parameterList
    : parameter (',' parameter)*
    ;

type
    : collectionType '<' innerType=type '>'
    | '@'? qualifiedName
    ;

collectionType
    : 'List' | 'Set' | 'Bag' | 'Collection'
    ;

service
    : 'Service' name serviceBody=genericBody?
    ;

repository
    : 'Repository' name repositoryBody?
    ;

repositoryBody
    : '{' repositoryMethod* '}'
    ;

repositoryMethod
    : visibility?
      (
          '@'? type name
          | name
      )
      ('(' parameterList? ')')?
      operationTail?
      ('throws' idList)?
      ';'?
    ;

visibility
    : 'public' | 'private' | 'protected'
    ;

genericBody
    : contentBlock
    ;

// --- Application & choreography ---

application
    : 'Application' '{' applicationElement* '}'
    ;

applicationElement
    : commandDecl | flow | service | coordination
    ;

commandDecl
    : 'Command' name ';'?
    ;

flow
    : 'Flow' name '{' flowStep* '}'
    ;

flowStep
    : flowCommandStep | flowEventStep | flowOperationStep
    ;

flowCommandStep
    : 'command' name flowCommandTail? ';'?
    ;

flowCommandTail
    : flowDelegate? flowEmitsClause?
    ;

flowEventStep
    : 'event' flowEventTriggerList 'triggers' flowInvocationList ';'?
    ;

flowEventTriggerList
    : name (transitionOperator name)*  // event A + B triggers...
    ;

flowOperationStep
    : 'operation' name flowOperationTail? ';'?
    ;

flowOperationTail
    : flowDelegate? flowEmitsClause?
    ;

flowDelegate
    : 'delegates' 'to' name stateTransition
    ;

flowInvocationList
    : flowInvocation (flowInvocationConnector)*
    ;

flowInvocationConnector
    : transitionOperator flowInvocation
    ;

flowInvocation
    : flowInvocationKind? name  // Kind is optional for subsequent invocations
    ;

flowInvocationKind
    : 'command' | 'operation'
    ;

flowEmitsClause
    : 'emits' 'event' flowEventList
    ;

flowEventList
    : name (transitionOperator name)*
    ;

coordination
    : 'Coordination' name '{' coordinationStep* '}'
    ;

coordinationStep
    : coordinationPath ';'?
    ;

coordinationPath
    : name ('::' name)*
    ;

stateTransition
    : '['
      (idList)?
      ('->' name (transitionOperator name)*)?
      ']'
    ;

transitionOperator
    : 'X' | '+' | 'O'
    ;

// --- Use Cases ---

useCase
    : 'UseCase' name '{' (useCaseBody | useCaseFreeText)* '}'
    ;

useCaseBody
    : useCaseActor
    | useCaseInteractionsBlock
    | useCaseBenefit
    | useCaseScope
    | useCaseLevel
    ;

useCaseActor
    : 'actor' STRING
    ;

useCaseInteractionsBlock
    : 'interactions' useCaseInteractionItem+
    ;

useCaseInteractionItem
    : useCaseReadOperation ','?  
    | STRING ','?
    | useCaseInteractionId ','?
    ;

useCaseInteractionId
    : name
    | READ
    | WITH
    | ITS
    ;

useCaseReadOperation
    : READ STRING WITH ITS STRING (',' STRING)*
    ;

useCaseFreeText
    : (~'}')+
    ;

userStory
    : 'UserStory' name '{' (userStoryBody | userStoryLine)* '}'
    ;

userStoryBody
    : 'As' ('a' | 'an')? STRING
      'I' 'want' 'to' (ID | 'do')? STRING
      'so' 'that' STRING
    ;

userStoryLine
    : (~'}')+
    ;

name
    : ID
    | 'X' | 'O' | 'U' | 'D' | 'S' | 'C' | 'P'
    | 'ACL' | 'CF' | 'OHS' | 'PL' | 'SK'
    ;

useCaseBenefit
    : 'benefit' STRING
    ;

useCaseScope
    : 'scope' STRING
    ;

useCaseLevel
    : 'level' STRING
    ;

// --- Stakeholders and Values ---

stakeholderSection
    : 'Stakeholders' 'of' name '{' stakeholderItem* '}'
    ;

stakeholderItem
    : stakeholderGroup | stakeholder
    ;

stakeholderGroup
    : 'StakeholderGroup' name ('{' stakeholder* '}')?
    ;

stakeholder
    : 'Stakeholder' name ('{' stakeholderAttribute* '}')?
    ;

stakeholderAttribute
    : 'influence' name
    | 'interest' name
    | 'priority' name
    | 'impact' name
    | consequences
    | consequenceItem
    ;

consequences
    : 'consequences' consequenceItem*
    ;

consequenceItem
    : ('good' | 'bad' | 'action') STRING name?
    ;

valueRegister
    : 'ValueRegister' name 'for' name '{' valueCluster* value* '}'
    ;

valueCluster
    : 'ValueCluster' name '{' valueClusterAttribute* value* '}'
    ;

valueClusterAttribute
    : 'core' name
    | 'demonstrator' STRING
    ;

value
    : 'Value' name '{' valueAttribute* valueStakeholder* '}'
    ;

valueAttribute
    : 'core' name
    | 'isCore'
    | 'demonstrator' STRING
    ;

valueStakeholder
    : 'Stakeholder' name '{' stakeholderAttribute* '}'
    ;

rawStatement
    : (~(';' | '{' | '}'))+ ';'?
    ;

// --- Helpers ---

idList
    : name (',' name)*
    ;

qualifiedName
    : name ('.' name)*
    ;

// --- Lexer Rules ---

// Keywords for UseCase interactions (must come before ID)
READ : 'read';
WITH : 'with';
ITS : 'its';

ID
    : '^'? [a-zA-Z_] [a-zA-Z0-9_]*
    ;

STRING
    : '"' ( '\\' . | ~[\\"] )* '"'
    | '\'' ( '\\' . | ~[\\'] )* '\''
    ;

// Comments
COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
