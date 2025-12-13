# Generated from CML.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CMLParser import CMLParser
else:
    from CMLParser import CMLParser

# This class defines a complete listener for a parse tree produced by CMLParser.
class CMLListener(ParseTreeListener):

    # Enter a parse tree produced by CMLParser#definitions.
    def enterDefinitions(self, ctx:CMLParser.DefinitionsContext):
        pass

    # Exit a parse tree produced by CMLParser#definitions.
    def exitDefinitions(self, ctx:CMLParser.DefinitionsContext):
        pass


    # Enter a parse tree produced by CMLParser#imports.
    def enterImports(self, ctx:CMLParser.ImportsContext):
        pass

    # Exit a parse tree produced by CMLParser#imports.
    def exitImports(self, ctx:CMLParser.ImportsContext):
        pass


    # Enter a parse tree produced by CMLParser#topLevel.
    def enterTopLevel(self, ctx:CMLParser.TopLevelContext):
        pass

    # Exit a parse tree produced by CMLParser#topLevel.
    def exitTopLevel(self, ctx:CMLParser.TopLevelContext):
        pass


    # Enter a parse tree produced by CMLParser#contextMap.
    def enterContextMap(self, ctx:CMLParser.ContextMapContext):
        pass

    # Exit a parse tree produced by CMLParser#contextMap.
    def exitContextMap(self, ctx:CMLParser.ContextMapContext):
        pass


    # Enter a parse tree produced by CMLParser#contextMapSetting.
    def enterContextMapSetting(self, ctx:CMLParser.ContextMapSettingContext):
        pass

    # Exit a parse tree produced by CMLParser#contextMapSetting.
    def exitContextMapSetting(self, ctx:CMLParser.ContextMapSettingContext):
        pass


    # Enter a parse tree produced by CMLParser#contextMapType.
    def enterContextMapType(self, ctx:CMLParser.ContextMapTypeContext):
        pass

    # Exit a parse tree produced by CMLParser#contextMapType.
    def exitContextMapType(self, ctx:CMLParser.ContextMapTypeContext):
        pass


    # Enter a parse tree produced by CMLParser#contextMapState.
    def enterContextMapState(self, ctx:CMLParser.ContextMapStateContext):
        pass

    # Exit a parse tree produced by CMLParser#contextMapState.
    def exitContextMapState(self, ctx:CMLParser.ContextMapStateContext):
        pass


    # Enter a parse tree produced by CMLParser#relationship.
    def enterRelationship(self, ctx:CMLParser.RelationshipContext):
        pass

    # Exit a parse tree produced by CMLParser#relationship.
    def exitRelationship(self, ctx:CMLParser.RelationshipContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipConnection.
    def enterRelationshipConnection(self, ctx:CMLParser.RelationshipConnectionContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipConnection.
    def exitRelationshipConnection(self, ctx:CMLParser.RelationshipConnectionContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipEndpoint.
    def enterRelationshipEndpoint(self, ctx:CMLParser.RelationshipEndpointContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipEndpoint.
    def exitRelationshipEndpoint(self, ctx:CMLParser.RelationshipEndpointContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipKeyword.
    def enterRelationshipKeyword(self, ctx:CMLParser.RelationshipKeywordContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipKeyword.
    def exitRelationshipKeyword(self, ctx:CMLParser.RelationshipKeywordContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipRoles.
    def enterRelationshipRoles(self, ctx:CMLParser.RelationshipRolesContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipRoles.
    def exitRelationshipRoles(self, ctx:CMLParser.RelationshipRolesContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipRole.
    def enterRelationshipRole(self, ctx:CMLParser.RelationshipRoleContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipRole.
    def exitRelationshipRole(self, ctx:CMLParser.RelationshipRoleContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipArrow.
    def enterRelationshipArrow(self, ctx:CMLParser.RelationshipArrowContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipArrow.
    def exitRelationshipArrow(self, ctx:CMLParser.RelationshipArrowContext):
        pass


    # Enter a parse tree produced by CMLParser#relationshipAttribute.
    def enterRelationshipAttribute(self, ctx:CMLParser.RelationshipAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#relationshipAttribute.
    def exitRelationshipAttribute(self, ctx:CMLParser.RelationshipAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#downstreamRights.
    def enterDownstreamRights(self, ctx:CMLParser.DownstreamRightsContext):
        pass

    # Exit a parse tree produced by CMLParser#downstreamRights.
    def exitDownstreamRights(self, ctx:CMLParser.DownstreamRightsContext):
        pass


    # Enter a parse tree produced by CMLParser#boundedContext.
    def enterBoundedContext(self, ctx:CMLParser.BoundedContextContext):
        pass

    # Exit a parse tree produced by CMLParser#boundedContext.
    def exitBoundedContext(self, ctx:CMLParser.BoundedContextContext):
        pass


    # Enter a parse tree produced by CMLParser#boundedContextAttribute.
    def enterBoundedContextAttribute(self, ctx:CMLParser.BoundedContextAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#boundedContextAttribute.
    def exitBoundedContextAttribute(self, ctx:CMLParser.BoundedContextAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#boundedContextType.
    def enterBoundedContextType(self, ctx:CMLParser.BoundedContextTypeContext):
        pass

    # Exit a parse tree produced by CMLParser#boundedContextType.
    def exitBoundedContextType(self, ctx:CMLParser.BoundedContextTypeContext):
        pass


    # Enter a parse tree produced by CMLParser#knowledgeLevel.
    def enterKnowledgeLevel(self, ctx:CMLParser.KnowledgeLevelContext):
        pass

    # Exit a parse tree produced by CMLParser#knowledgeLevel.
    def exitKnowledgeLevel(self, ctx:CMLParser.KnowledgeLevelContext):
        pass


    # Enter a parse tree produced by CMLParser#domain.
    def enterDomain(self, ctx:CMLParser.DomainContext):
        pass

    # Exit a parse tree produced by CMLParser#domain.
    def exitDomain(self, ctx:CMLParser.DomainContext):
        pass


    # Enter a parse tree produced by CMLParser#subdomain.
    def enterSubdomain(self, ctx:CMLParser.SubdomainContext):
        pass

    # Exit a parse tree produced by CMLParser#subdomain.
    def exitSubdomain(self, ctx:CMLParser.SubdomainContext):
        pass


    # Enter a parse tree produced by CMLParser#subdomainType.
    def enterSubdomainType(self, ctx:CMLParser.SubdomainTypeContext):
        pass

    # Exit a parse tree produced by CMLParser#subdomainType.
    def exitSubdomainType(self, ctx:CMLParser.SubdomainTypeContext):
        pass


    # Enter a parse tree produced by CMLParser#module.
    def enterModule(self, ctx:CMLParser.ModuleContext):
        pass

    # Exit a parse tree produced by CMLParser#module.
    def exitModule(self, ctx:CMLParser.ModuleContext):
        pass


    # Enter a parse tree produced by CMLParser#aggregate.
    def enterAggregate(self, ctx:CMLParser.AggregateContext):
        pass

    # Exit a parse tree produced by CMLParser#aggregate.
    def exitAggregate(self, ctx:CMLParser.AggregateContext):
        pass


    # Enter a parse tree produced by CMLParser#domainObject.
    def enterDomainObject(self, ctx:CMLParser.DomainObjectContext):
        pass

    # Exit a parse tree produced by CMLParser#domainObject.
    def exitDomainObject(self, ctx:CMLParser.DomainObjectContext):
        pass


    # Enter a parse tree produced by CMLParser#simpleDomainObjectOrEnum.
    def enterSimpleDomainObjectOrEnum(self, ctx:CMLParser.SimpleDomainObjectOrEnumContext):
        pass

    # Exit a parse tree produced by CMLParser#simpleDomainObjectOrEnum.
    def exitSimpleDomainObjectOrEnum(self, ctx:CMLParser.SimpleDomainObjectOrEnumContext):
        pass


    # Enter a parse tree produced by CMLParser#simpleDomainObject.
    def enterSimpleDomainObject(self, ctx:CMLParser.SimpleDomainObjectContext):
        pass

    # Exit a parse tree produced by CMLParser#simpleDomainObject.
    def exitSimpleDomainObject(self, ctx:CMLParser.SimpleDomainObjectContext):
        pass


    # Enter a parse tree produced by CMLParser#entity.
    def enterEntity(self, ctx:CMLParser.EntityContext):
        pass

    # Exit a parse tree produced by CMLParser#entity.
    def exitEntity(self, ctx:CMLParser.EntityContext):
        pass


    # Enter a parse tree produced by CMLParser#entityBody.
    def enterEntityBody(self, ctx:CMLParser.EntityBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#entityBody.
    def exitEntityBody(self, ctx:CMLParser.EntityBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#valueObject.
    def enterValueObject(self, ctx:CMLParser.ValueObjectContext):
        pass

    # Exit a parse tree produced by CMLParser#valueObject.
    def exitValueObject(self, ctx:CMLParser.ValueObjectContext):
        pass


    # Enter a parse tree produced by CMLParser#valueObjectBody.
    def enterValueObjectBody(self, ctx:CMLParser.ValueObjectBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#valueObjectBody.
    def exitValueObjectBody(self, ctx:CMLParser.ValueObjectBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#domainEvent.
    def enterDomainEvent(self, ctx:CMLParser.DomainEventContext):
        pass

    # Exit a parse tree produced by CMLParser#domainEvent.
    def exitDomainEvent(self, ctx:CMLParser.DomainEventContext):
        pass


    # Enter a parse tree produced by CMLParser#domainEventBody.
    def enterDomainEventBody(self, ctx:CMLParser.DomainEventBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#domainEventBody.
    def exitDomainEventBody(self, ctx:CMLParser.DomainEventBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#commandEvent.
    def enterCommandEvent(self, ctx:CMLParser.CommandEventContext):
        pass

    # Exit a parse tree produced by CMLParser#commandEvent.
    def exitCommandEvent(self, ctx:CMLParser.CommandEventContext):
        pass


    # Enter a parse tree produced by CMLParser#commandEventBody.
    def enterCommandEventBody(self, ctx:CMLParser.CommandEventBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#commandEventBody.
    def exitCommandEventBody(self, ctx:CMLParser.CommandEventBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#dataTransferObject.
    def enterDataTransferObject(self, ctx:CMLParser.DataTransferObjectContext):
        pass

    # Exit a parse tree produced by CMLParser#dataTransferObject.
    def exitDataTransferObject(self, ctx:CMLParser.DataTransferObjectContext):
        pass


    # Enter a parse tree produced by CMLParser#dtoBody.
    def enterDtoBody(self, ctx:CMLParser.DtoBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#dtoBody.
    def exitDtoBody(self, ctx:CMLParser.DtoBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#enumDecl.
    def enterEnumDecl(self, ctx:CMLParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by CMLParser#enumDecl.
    def exitEnumDecl(self, ctx:CMLParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by CMLParser#feature.
    def enterFeature(self, ctx:CMLParser.FeatureContext):
        pass

    # Exit a parse tree produced by CMLParser#feature.
    def exitFeature(self, ctx:CMLParser.FeatureContext):
        pass


    # Enter a parse tree produced by CMLParser#attribute.
    def enterAttribute(self, ctx:CMLParser.AttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#attribute.
    def exitAttribute(self, ctx:CMLParser.AttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#operation.
    def enterOperation(self, ctx:CMLParser.OperationContext):
        pass

    # Exit a parse tree produced by CMLParser#operation.
    def exitOperation(self, ctx:CMLParser.OperationContext):
        pass


    # Enter a parse tree produced by CMLParser#operationHint.
    def enterOperationHint(self, ctx:CMLParser.OperationHintContext):
        pass

    # Exit a parse tree produced by CMLParser#operationHint.
    def exitOperationHint(self, ctx:CMLParser.OperationHintContext):
        pass


    # Enter a parse tree produced by CMLParser#operationHintType.
    def enterOperationHintType(self, ctx:CMLParser.OperationHintTypeContext):
        pass

    # Exit a parse tree produced by CMLParser#operationHintType.
    def exitOperationHintType(self, ctx:CMLParser.OperationHintTypeContext):
        pass


    # Enter a parse tree produced by CMLParser#operationTail.
    def enterOperationTail(self, ctx:CMLParser.OperationTailContext):
        pass

    # Exit a parse tree produced by CMLParser#operationTail.
    def exitOperationTail(self, ctx:CMLParser.OperationTailContext):
        pass


    # Enter a parse tree produced by CMLParser#contentBlock.
    def enterContentBlock(self, ctx:CMLParser.ContentBlockContext):
        pass

    # Exit a parse tree produced by CMLParser#contentBlock.
    def exitContentBlock(self, ctx:CMLParser.ContentBlockContext):
        pass


    # Enter a parse tree produced by CMLParser#contentEntry.
    def enterContentEntry(self, ctx:CMLParser.ContentEntryContext):
        pass

    # Exit a parse tree produced by CMLParser#contentEntry.
    def exitContentEntry(self, ctx:CMLParser.ContentEntryContext):
        pass


    # Enter a parse tree produced by CMLParser#subdomainAttribute.
    def enterSubdomainAttribute(self, ctx:CMLParser.SubdomainAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#subdomainAttribute.
    def exitSubdomainAttribute(self, ctx:CMLParser.SubdomainAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#contentItem.
    def enterContentItem(self, ctx:CMLParser.ContentItemContext):
        pass

    # Exit a parse tree produced by CMLParser#contentItem.
    def exitContentItem(self, ctx:CMLParser.ContentItemContext):
        pass


    # Enter a parse tree produced by CMLParser#ownerDecl.
    def enterOwnerDecl(self, ctx:CMLParser.OwnerDeclContext):
        pass

    # Exit a parse tree produced by CMLParser#ownerDecl.
    def exitOwnerDecl(self, ctx:CMLParser.OwnerDeclContext):
        pass


    # Enter a parse tree produced by CMLParser#setting.
    def enterSetting(self, ctx:CMLParser.SettingContext):
        pass

    # Exit a parse tree produced by CMLParser#setting.
    def exitSetting(self, ctx:CMLParser.SettingContext):
        pass


    # Enter a parse tree produced by CMLParser#parameter.
    def enterParameter(self, ctx:CMLParser.ParameterContext):
        pass

    # Exit a parse tree produced by CMLParser#parameter.
    def exitParameter(self, ctx:CMLParser.ParameterContext):
        pass


    # Enter a parse tree produced by CMLParser#parameterList.
    def enterParameterList(self, ctx:CMLParser.ParameterListContext):
        pass

    # Exit a parse tree produced by CMLParser#parameterList.
    def exitParameterList(self, ctx:CMLParser.ParameterListContext):
        pass


    # Enter a parse tree produced by CMLParser#type.
    def enterType(self, ctx:CMLParser.TypeContext):
        pass

    # Exit a parse tree produced by CMLParser#type.
    def exitType(self, ctx:CMLParser.TypeContext):
        pass


    # Enter a parse tree produced by CMLParser#collectionType.
    def enterCollectionType(self, ctx:CMLParser.CollectionTypeContext):
        pass

    # Exit a parse tree produced by CMLParser#collectionType.
    def exitCollectionType(self, ctx:CMLParser.CollectionTypeContext):
        pass


    # Enter a parse tree produced by CMLParser#service.
    def enterService(self, ctx:CMLParser.ServiceContext):
        pass

    # Exit a parse tree produced by CMLParser#service.
    def exitService(self, ctx:CMLParser.ServiceContext):
        pass


    # Enter a parse tree produced by CMLParser#repository.
    def enterRepository(self, ctx:CMLParser.RepositoryContext):
        pass

    # Exit a parse tree produced by CMLParser#repository.
    def exitRepository(self, ctx:CMLParser.RepositoryContext):
        pass


    # Enter a parse tree produced by CMLParser#repositoryBody.
    def enterRepositoryBody(self, ctx:CMLParser.RepositoryBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#repositoryBody.
    def exitRepositoryBody(self, ctx:CMLParser.RepositoryBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#repositoryMethod.
    def enterRepositoryMethod(self, ctx:CMLParser.RepositoryMethodContext):
        pass

    # Exit a parse tree produced by CMLParser#repositoryMethod.
    def exitRepositoryMethod(self, ctx:CMLParser.RepositoryMethodContext):
        pass


    # Enter a parse tree produced by CMLParser#visibility.
    def enterVisibility(self, ctx:CMLParser.VisibilityContext):
        pass

    # Exit a parse tree produced by CMLParser#visibility.
    def exitVisibility(self, ctx:CMLParser.VisibilityContext):
        pass


    # Enter a parse tree produced by CMLParser#genericBody.
    def enterGenericBody(self, ctx:CMLParser.GenericBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#genericBody.
    def exitGenericBody(self, ctx:CMLParser.GenericBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#application.
    def enterApplication(self, ctx:CMLParser.ApplicationContext):
        pass

    # Exit a parse tree produced by CMLParser#application.
    def exitApplication(self, ctx:CMLParser.ApplicationContext):
        pass


    # Enter a parse tree produced by CMLParser#applicationElement.
    def enterApplicationElement(self, ctx:CMLParser.ApplicationElementContext):
        pass

    # Exit a parse tree produced by CMLParser#applicationElement.
    def exitApplicationElement(self, ctx:CMLParser.ApplicationElementContext):
        pass


    # Enter a parse tree produced by CMLParser#commandDecl.
    def enterCommandDecl(self, ctx:CMLParser.CommandDeclContext):
        pass

    # Exit a parse tree produced by CMLParser#commandDecl.
    def exitCommandDecl(self, ctx:CMLParser.CommandDeclContext):
        pass


    # Enter a parse tree produced by CMLParser#flow.
    def enterFlow(self, ctx:CMLParser.FlowContext):
        pass

    # Exit a parse tree produced by CMLParser#flow.
    def exitFlow(self, ctx:CMLParser.FlowContext):
        pass


    # Enter a parse tree produced by CMLParser#flowStep.
    def enterFlowStep(self, ctx:CMLParser.FlowStepContext):
        pass

    # Exit a parse tree produced by CMLParser#flowStep.
    def exitFlowStep(self, ctx:CMLParser.FlowStepContext):
        pass


    # Enter a parse tree produced by CMLParser#flowCommandStep.
    def enterFlowCommandStep(self, ctx:CMLParser.FlowCommandStepContext):
        pass

    # Exit a parse tree produced by CMLParser#flowCommandStep.
    def exitFlowCommandStep(self, ctx:CMLParser.FlowCommandStepContext):
        pass


    # Enter a parse tree produced by CMLParser#flowCommandTail.
    def enterFlowCommandTail(self, ctx:CMLParser.FlowCommandTailContext):
        pass

    # Exit a parse tree produced by CMLParser#flowCommandTail.
    def exitFlowCommandTail(self, ctx:CMLParser.FlowCommandTailContext):
        pass


    # Enter a parse tree produced by CMLParser#flowEventStep.
    def enterFlowEventStep(self, ctx:CMLParser.FlowEventStepContext):
        pass

    # Exit a parse tree produced by CMLParser#flowEventStep.
    def exitFlowEventStep(self, ctx:CMLParser.FlowEventStepContext):
        pass


    # Enter a parse tree produced by CMLParser#flowEventTriggerList.
    def enterFlowEventTriggerList(self, ctx:CMLParser.FlowEventTriggerListContext):
        pass

    # Exit a parse tree produced by CMLParser#flowEventTriggerList.
    def exitFlowEventTriggerList(self, ctx:CMLParser.FlowEventTriggerListContext):
        pass


    # Enter a parse tree produced by CMLParser#flowOperationStep.
    def enterFlowOperationStep(self, ctx:CMLParser.FlowOperationStepContext):
        pass

    # Exit a parse tree produced by CMLParser#flowOperationStep.
    def exitFlowOperationStep(self, ctx:CMLParser.FlowOperationStepContext):
        pass


    # Enter a parse tree produced by CMLParser#flowOperationTail.
    def enterFlowOperationTail(self, ctx:CMLParser.FlowOperationTailContext):
        pass

    # Exit a parse tree produced by CMLParser#flowOperationTail.
    def exitFlowOperationTail(self, ctx:CMLParser.FlowOperationTailContext):
        pass


    # Enter a parse tree produced by CMLParser#flowDelegate.
    def enterFlowDelegate(self, ctx:CMLParser.FlowDelegateContext):
        pass

    # Exit a parse tree produced by CMLParser#flowDelegate.
    def exitFlowDelegate(self, ctx:CMLParser.FlowDelegateContext):
        pass


    # Enter a parse tree produced by CMLParser#flowInvocationList.
    def enterFlowInvocationList(self, ctx:CMLParser.FlowInvocationListContext):
        pass

    # Exit a parse tree produced by CMLParser#flowInvocationList.
    def exitFlowInvocationList(self, ctx:CMLParser.FlowInvocationListContext):
        pass


    # Enter a parse tree produced by CMLParser#flowInvocationConnector.
    def enterFlowInvocationConnector(self, ctx:CMLParser.FlowInvocationConnectorContext):
        pass

    # Exit a parse tree produced by CMLParser#flowInvocationConnector.
    def exitFlowInvocationConnector(self, ctx:CMLParser.FlowInvocationConnectorContext):
        pass


    # Enter a parse tree produced by CMLParser#flowInvocation.
    def enterFlowInvocation(self, ctx:CMLParser.FlowInvocationContext):
        pass

    # Exit a parse tree produced by CMLParser#flowInvocation.
    def exitFlowInvocation(self, ctx:CMLParser.FlowInvocationContext):
        pass


    # Enter a parse tree produced by CMLParser#flowInvocationKind.
    def enterFlowInvocationKind(self, ctx:CMLParser.FlowInvocationKindContext):
        pass

    # Exit a parse tree produced by CMLParser#flowInvocationKind.
    def exitFlowInvocationKind(self, ctx:CMLParser.FlowInvocationKindContext):
        pass


    # Enter a parse tree produced by CMLParser#flowEmitsClause.
    def enterFlowEmitsClause(self, ctx:CMLParser.FlowEmitsClauseContext):
        pass

    # Exit a parse tree produced by CMLParser#flowEmitsClause.
    def exitFlowEmitsClause(self, ctx:CMLParser.FlowEmitsClauseContext):
        pass


    # Enter a parse tree produced by CMLParser#flowEventList.
    def enterFlowEventList(self, ctx:CMLParser.FlowEventListContext):
        pass

    # Exit a parse tree produced by CMLParser#flowEventList.
    def exitFlowEventList(self, ctx:CMLParser.FlowEventListContext):
        pass


    # Enter a parse tree produced by CMLParser#coordination.
    def enterCoordination(self, ctx:CMLParser.CoordinationContext):
        pass

    # Exit a parse tree produced by CMLParser#coordination.
    def exitCoordination(self, ctx:CMLParser.CoordinationContext):
        pass


    # Enter a parse tree produced by CMLParser#coordinationStep.
    def enterCoordinationStep(self, ctx:CMLParser.CoordinationStepContext):
        pass

    # Exit a parse tree produced by CMLParser#coordinationStep.
    def exitCoordinationStep(self, ctx:CMLParser.CoordinationStepContext):
        pass


    # Enter a parse tree produced by CMLParser#coordinationPath.
    def enterCoordinationPath(self, ctx:CMLParser.CoordinationPathContext):
        pass

    # Exit a parse tree produced by CMLParser#coordinationPath.
    def exitCoordinationPath(self, ctx:CMLParser.CoordinationPathContext):
        pass


    # Enter a parse tree produced by CMLParser#stateTransition.
    def enterStateTransition(self, ctx:CMLParser.StateTransitionContext):
        pass

    # Exit a parse tree produced by CMLParser#stateTransition.
    def exitStateTransition(self, ctx:CMLParser.StateTransitionContext):
        pass


    # Enter a parse tree produced by CMLParser#transitionOperator.
    def enterTransitionOperator(self, ctx:CMLParser.TransitionOperatorContext):
        pass

    # Exit a parse tree produced by CMLParser#transitionOperator.
    def exitTransitionOperator(self, ctx:CMLParser.TransitionOperatorContext):
        pass


    # Enter a parse tree produced by CMLParser#useCase.
    def enterUseCase(self, ctx:CMLParser.UseCaseContext):
        pass

    # Exit a parse tree produced by CMLParser#useCase.
    def exitUseCase(self, ctx:CMLParser.UseCaseContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseBody.
    def enterUseCaseBody(self, ctx:CMLParser.UseCaseBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseBody.
    def exitUseCaseBody(self, ctx:CMLParser.UseCaseBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseActor.
    def enterUseCaseActor(self, ctx:CMLParser.UseCaseActorContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseActor.
    def exitUseCaseActor(self, ctx:CMLParser.UseCaseActorContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseInteractionsBlock.
    def enterUseCaseInteractionsBlock(self, ctx:CMLParser.UseCaseInteractionsBlockContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseInteractionsBlock.
    def exitUseCaseInteractionsBlock(self, ctx:CMLParser.UseCaseInteractionsBlockContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseInteractionItem.
    def enterUseCaseInteractionItem(self, ctx:CMLParser.UseCaseInteractionItemContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseInteractionItem.
    def exitUseCaseInteractionItem(self, ctx:CMLParser.UseCaseInteractionItemContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseInteractionId.
    def enterUseCaseInteractionId(self, ctx:CMLParser.UseCaseInteractionIdContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseInteractionId.
    def exitUseCaseInteractionId(self, ctx:CMLParser.UseCaseInteractionIdContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseReadOperation.
    def enterUseCaseReadOperation(self, ctx:CMLParser.UseCaseReadOperationContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseReadOperation.
    def exitUseCaseReadOperation(self, ctx:CMLParser.UseCaseReadOperationContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseFreeText.
    def enterUseCaseFreeText(self, ctx:CMLParser.UseCaseFreeTextContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseFreeText.
    def exitUseCaseFreeText(self, ctx:CMLParser.UseCaseFreeTextContext):
        pass


    # Enter a parse tree produced by CMLParser#userStory.
    def enterUserStory(self, ctx:CMLParser.UserStoryContext):
        pass

    # Exit a parse tree produced by CMLParser#userStory.
    def exitUserStory(self, ctx:CMLParser.UserStoryContext):
        pass


    # Enter a parse tree produced by CMLParser#userStoryBody.
    def enterUserStoryBody(self, ctx:CMLParser.UserStoryBodyContext):
        pass

    # Exit a parse tree produced by CMLParser#userStoryBody.
    def exitUserStoryBody(self, ctx:CMLParser.UserStoryBodyContext):
        pass


    # Enter a parse tree produced by CMLParser#userStoryLine.
    def enterUserStoryLine(self, ctx:CMLParser.UserStoryLineContext):
        pass

    # Exit a parse tree produced by CMLParser#userStoryLine.
    def exitUserStoryLine(self, ctx:CMLParser.UserStoryLineContext):
        pass


    # Enter a parse tree produced by CMLParser#name.
    def enterName(self, ctx:CMLParser.NameContext):
        pass

    # Exit a parse tree produced by CMLParser#name.
    def exitName(self, ctx:CMLParser.NameContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseBenefit.
    def enterUseCaseBenefit(self, ctx:CMLParser.UseCaseBenefitContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseBenefit.
    def exitUseCaseBenefit(self, ctx:CMLParser.UseCaseBenefitContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseScope.
    def enterUseCaseScope(self, ctx:CMLParser.UseCaseScopeContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseScope.
    def exitUseCaseScope(self, ctx:CMLParser.UseCaseScopeContext):
        pass


    # Enter a parse tree produced by CMLParser#useCaseLevel.
    def enterUseCaseLevel(self, ctx:CMLParser.UseCaseLevelContext):
        pass

    # Exit a parse tree produced by CMLParser#useCaseLevel.
    def exitUseCaseLevel(self, ctx:CMLParser.UseCaseLevelContext):
        pass


    # Enter a parse tree produced by CMLParser#stakeholderSection.
    def enterStakeholderSection(self, ctx:CMLParser.StakeholderSectionContext):
        pass

    # Exit a parse tree produced by CMLParser#stakeholderSection.
    def exitStakeholderSection(self, ctx:CMLParser.StakeholderSectionContext):
        pass


    # Enter a parse tree produced by CMLParser#stakeholderItem.
    def enterStakeholderItem(self, ctx:CMLParser.StakeholderItemContext):
        pass

    # Exit a parse tree produced by CMLParser#stakeholderItem.
    def exitStakeholderItem(self, ctx:CMLParser.StakeholderItemContext):
        pass


    # Enter a parse tree produced by CMLParser#stakeholderGroup.
    def enterStakeholderGroup(self, ctx:CMLParser.StakeholderGroupContext):
        pass

    # Exit a parse tree produced by CMLParser#stakeholderGroup.
    def exitStakeholderGroup(self, ctx:CMLParser.StakeholderGroupContext):
        pass


    # Enter a parse tree produced by CMLParser#stakeholder.
    def enterStakeholder(self, ctx:CMLParser.StakeholderContext):
        pass

    # Exit a parse tree produced by CMLParser#stakeholder.
    def exitStakeholder(self, ctx:CMLParser.StakeholderContext):
        pass


    # Enter a parse tree produced by CMLParser#stakeholderAttribute.
    def enterStakeholderAttribute(self, ctx:CMLParser.StakeholderAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#stakeholderAttribute.
    def exitStakeholderAttribute(self, ctx:CMLParser.StakeholderAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#consequences.
    def enterConsequences(self, ctx:CMLParser.ConsequencesContext):
        pass

    # Exit a parse tree produced by CMLParser#consequences.
    def exitConsequences(self, ctx:CMLParser.ConsequencesContext):
        pass


    # Enter a parse tree produced by CMLParser#consequenceItem.
    def enterConsequenceItem(self, ctx:CMLParser.ConsequenceItemContext):
        pass

    # Exit a parse tree produced by CMLParser#consequenceItem.
    def exitConsequenceItem(self, ctx:CMLParser.ConsequenceItemContext):
        pass


    # Enter a parse tree produced by CMLParser#valueRegister.
    def enterValueRegister(self, ctx:CMLParser.ValueRegisterContext):
        pass

    # Exit a parse tree produced by CMLParser#valueRegister.
    def exitValueRegister(self, ctx:CMLParser.ValueRegisterContext):
        pass


    # Enter a parse tree produced by CMLParser#valueCluster.
    def enterValueCluster(self, ctx:CMLParser.ValueClusterContext):
        pass

    # Exit a parse tree produced by CMLParser#valueCluster.
    def exitValueCluster(self, ctx:CMLParser.ValueClusterContext):
        pass


    # Enter a parse tree produced by CMLParser#valueClusterAttribute.
    def enterValueClusterAttribute(self, ctx:CMLParser.ValueClusterAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#valueClusterAttribute.
    def exitValueClusterAttribute(self, ctx:CMLParser.ValueClusterAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#value.
    def enterValue(self, ctx:CMLParser.ValueContext):
        pass

    # Exit a parse tree produced by CMLParser#value.
    def exitValue(self, ctx:CMLParser.ValueContext):
        pass


    # Enter a parse tree produced by CMLParser#valueAttribute.
    def enterValueAttribute(self, ctx:CMLParser.ValueAttributeContext):
        pass

    # Exit a parse tree produced by CMLParser#valueAttribute.
    def exitValueAttribute(self, ctx:CMLParser.ValueAttributeContext):
        pass


    # Enter a parse tree produced by CMLParser#valueStakeholder.
    def enterValueStakeholder(self, ctx:CMLParser.ValueStakeholderContext):
        pass

    # Exit a parse tree produced by CMLParser#valueStakeholder.
    def exitValueStakeholder(self, ctx:CMLParser.ValueStakeholderContext):
        pass


    # Enter a parse tree produced by CMLParser#rawStatement.
    def enterRawStatement(self, ctx:CMLParser.RawStatementContext):
        pass

    # Exit a parse tree produced by CMLParser#rawStatement.
    def exitRawStatement(self, ctx:CMLParser.RawStatementContext):
        pass


    # Enter a parse tree produced by CMLParser#idList.
    def enterIdList(self, ctx:CMLParser.IdListContext):
        pass

    # Exit a parse tree produced by CMLParser#idList.
    def exitIdList(self, ctx:CMLParser.IdListContext):
        pass


    # Enter a parse tree produced by CMLParser#qualifiedName.
    def enterQualifiedName(self, ctx:CMLParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by CMLParser#qualifiedName.
    def exitQualifiedName(self, ctx:CMLParser.QualifiedNameContext):
        pass



del CMLParser