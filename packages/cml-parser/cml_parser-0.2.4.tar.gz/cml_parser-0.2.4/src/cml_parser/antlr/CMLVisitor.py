# Generated from CML.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CMLParser import CMLParser
else:
    from CMLParser import CMLParser

# This class defines a complete generic visitor for a parse tree produced by CMLParser.

class CMLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CMLParser#definitions.
    def visitDefinitions(self, ctx:CMLParser.DefinitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#imports.
    def visitImports(self, ctx:CMLParser.ImportsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#topLevel.
    def visitTopLevel(self, ctx:CMLParser.TopLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contextMap.
    def visitContextMap(self, ctx:CMLParser.ContextMapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contextMapSetting.
    def visitContextMapSetting(self, ctx:CMLParser.ContextMapSettingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contextMapType.
    def visitContextMapType(self, ctx:CMLParser.ContextMapTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contextMapState.
    def visitContextMapState(self, ctx:CMLParser.ContextMapStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationship.
    def visitRelationship(self, ctx:CMLParser.RelationshipContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipConnection.
    def visitRelationshipConnection(self, ctx:CMLParser.RelationshipConnectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipEndpoint.
    def visitRelationshipEndpoint(self, ctx:CMLParser.RelationshipEndpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipKeyword.
    def visitRelationshipKeyword(self, ctx:CMLParser.RelationshipKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipRoles.
    def visitRelationshipRoles(self, ctx:CMLParser.RelationshipRolesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipRole.
    def visitRelationshipRole(self, ctx:CMLParser.RelationshipRoleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipArrow.
    def visitRelationshipArrow(self, ctx:CMLParser.RelationshipArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#relationshipAttribute.
    def visitRelationshipAttribute(self, ctx:CMLParser.RelationshipAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#downstreamRights.
    def visitDownstreamRights(self, ctx:CMLParser.DownstreamRightsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#boundedContext.
    def visitBoundedContext(self, ctx:CMLParser.BoundedContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#boundedContextAttribute.
    def visitBoundedContextAttribute(self, ctx:CMLParser.BoundedContextAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#boundedContextType.
    def visitBoundedContextType(self, ctx:CMLParser.BoundedContextTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#knowledgeLevel.
    def visitKnowledgeLevel(self, ctx:CMLParser.KnowledgeLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#domain.
    def visitDomain(self, ctx:CMLParser.DomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#subdomain.
    def visitSubdomain(self, ctx:CMLParser.SubdomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#subdomainType.
    def visitSubdomainType(self, ctx:CMLParser.SubdomainTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#module.
    def visitModule(self, ctx:CMLParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#aggregate.
    def visitAggregate(self, ctx:CMLParser.AggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#domainObject.
    def visitDomainObject(self, ctx:CMLParser.DomainObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#simpleDomainObjectOrEnum.
    def visitSimpleDomainObjectOrEnum(self, ctx:CMLParser.SimpleDomainObjectOrEnumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#simpleDomainObject.
    def visitSimpleDomainObject(self, ctx:CMLParser.SimpleDomainObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#entity.
    def visitEntity(self, ctx:CMLParser.EntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#entityBody.
    def visitEntityBody(self, ctx:CMLParser.EntityBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueObject.
    def visitValueObject(self, ctx:CMLParser.ValueObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueObjectBody.
    def visitValueObjectBody(self, ctx:CMLParser.ValueObjectBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#domainEvent.
    def visitDomainEvent(self, ctx:CMLParser.DomainEventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#domainEventBody.
    def visitDomainEventBody(self, ctx:CMLParser.DomainEventBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#commandEvent.
    def visitCommandEvent(self, ctx:CMLParser.CommandEventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#commandEventBody.
    def visitCommandEventBody(self, ctx:CMLParser.CommandEventBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#dataTransferObject.
    def visitDataTransferObject(self, ctx:CMLParser.DataTransferObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#dtoBody.
    def visitDtoBody(self, ctx:CMLParser.DtoBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#enumDecl.
    def visitEnumDecl(self, ctx:CMLParser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#feature.
    def visitFeature(self, ctx:CMLParser.FeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#attribute.
    def visitAttribute(self, ctx:CMLParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#operation.
    def visitOperation(self, ctx:CMLParser.OperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#operationHint.
    def visitOperationHint(self, ctx:CMLParser.OperationHintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#operationHintType.
    def visitOperationHintType(self, ctx:CMLParser.OperationHintTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#operationTail.
    def visitOperationTail(self, ctx:CMLParser.OperationTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contentBlock.
    def visitContentBlock(self, ctx:CMLParser.ContentBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contentEntry.
    def visitContentEntry(self, ctx:CMLParser.ContentEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#subdomainAttribute.
    def visitSubdomainAttribute(self, ctx:CMLParser.SubdomainAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#contentItem.
    def visitContentItem(self, ctx:CMLParser.ContentItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#ownerDecl.
    def visitOwnerDecl(self, ctx:CMLParser.OwnerDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#setting.
    def visitSetting(self, ctx:CMLParser.SettingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#parameter.
    def visitParameter(self, ctx:CMLParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#parameterList.
    def visitParameterList(self, ctx:CMLParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#type.
    def visitType(self, ctx:CMLParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#collectionType.
    def visitCollectionType(self, ctx:CMLParser.CollectionTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#service.
    def visitService(self, ctx:CMLParser.ServiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#repository.
    def visitRepository(self, ctx:CMLParser.RepositoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#repositoryBody.
    def visitRepositoryBody(self, ctx:CMLParser.RepositoryBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#repositoryMethod.
    def visitRepositoryMethod(self, ctx:CMLParser.RepositoryMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#visibility.
    def visitVisibility(self, ctx:CMLParser.VisibilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#genericBody.
    def visitGenericBody(self, ctx:CMLParser.GenericBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#application.
    def visitApplication(self, ctx:CMLParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#applicationElement.
    def visitApplicationElement(self, ctx:CMLParser.ApplicationElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#commandDecl.
    def visitCommandDecl(self, ctx:CMLParser.CommandDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flow.
    def visitFlow(self, ctx:CMLParser.FlowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowStep.
    def visitFlowStep(self, ctx:CMLParser.FlowStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowCommandStep.
    def visitFlowCommandStep(self, ctx:CMLParser.FlowCommandStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowCommandTail.
    def visitFlowCommandTail(self, ctx:CMLParser.FlowCommandTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowEventStep.
    def visitFlowEventStep(self, ctx:CMLParser.FlowEventStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowEventTriggerList.
    def visitFlowEventTriggerList(self, ctx:CMLParser.FlowEventTriggerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowOperationStep.
    def visitFlowOperationStep(self, ctx:CMLParser.FlowOperationStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowOperationTail.
    def visitFlowOperationTail(self, ctx:CMLParser.FlowOperationTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowDelegate.
    def visitFlowDelegate(self, ctx:CMLParser.FlowDelegateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowInvocationList.
    def visitFlowInvocationList(self, ctx:CMLParser.FlowInvocationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowInvocationConnector.
    def visitFlowInvocationConnector(self, ctx:CMLParser.FlowInvocationConnectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowInvocation.
    def visitFlowInvocation(self, ctx:CMLParser.FlowInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowInvocationKind.
    def visitFlowInvocationKind(self, ctx:CMLParser.FlowInvocationKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowEmitsClause.
    def visitFlowEmitsClause(self, ctx:CMLParser.FlowEmitsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#flowEventList.
    def visitFlowEventList(self, ctx:CMLParser.FlowEventListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#coordination.
    def visitCoordination(self, ctx:CMLParser.CoordinationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#coordinationStep.
    def visitCoordinationStep(self, ctx:CMLParser.CoordinationStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#coordinationPath.
    def visitCoordinationPath(self, ctx:CMLParser.CoordinationPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stateTransition.
    def visitStateTransition(self, ctx:CMLParser.StateTransitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#transitionOperator.
    def visitTransitionOperator(self, ctx:CMLParser.TransitionOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCase.
    def visitUseCase(self, ctx:CMLParser.UseCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseBody.
    def visitUseCaseBody(self, ctx:CMLParser.UseCaseBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseActor.
    def visitUseCaseActor(self, ctx:CMLParser.UseCaseActorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseInteractionsBlock.
    def visitUseCaseInteractionsBlock(self, ctx:CMLParser.UseCaseInteractionsBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseInteractionItem.
    def visitUseCaseInteractionItem(self, ctx:CMLParser.UseCaseInteractionItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseInteractionId.
    def visitUseCaseInteractionId(self, ctx:CMLParser.UseCaseInteractionIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseReadOperation.
    def visitUseCaseReadOperation(self, ctx:CMLParser.UseCaseReadOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseFreeText.
    def visitUseCaseFreeText(self, ctx:CMLParser.UseCaseFreeTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#userStory.
    def visitUserStory(self, ctx:CMLParser.UserStoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#userStoryBody.
    def visitUserStoryBody(self, ctx:CMLParser.UserStoryBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#userStoryLine.
    def visitUserStoryLine(self, ctx:CMLParser.UserStoryLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#name.
    def visitName(self, ctx:CMLParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseBenefit.
    def visitUseCaseBenefit(self, ctx:CMLParser.UseCaseBenefitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseScope.
    def visitUseCaseScope(self, ctx:CMLParser.UseCaseScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#useCaseLevel.
    def visitUseCaseLevel(self, ctx:CMLParser.UseCaseLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stakeholderSection.
    def visitStakeholderSection(self, ctx:CMLParser.StakeholderSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stakeholderItem.
    def visitStakeholderItem(self, ctx:CMLParser.StakeholderItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stakeholderGroup.
    def visitStakeholderGroup(self, ctx:CMLParser.StakeholderGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stakeholder.
    def visitStakeholder(self, ctx:CMLParser.StakeholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#stakeholderAttribute.
    def visitStakeholderAttribute(self, ctx:CMLParser.StakeholderAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#consequences.
    def visitConsequences(self, ctx:CMLParser.ConsequencesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#consequenceItem.
    def visitConsequenceItem(self, ctx:CMLParser.ConsequenceItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueRegister.
    def visitValueRegister(self, ctx:CMLParser.ValueRegisterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueCluster.
    def visitValueCluster(self, ctx:CMLParser.ValueClusterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueClusterAttribute.
    def visitValueClusterAttribute(self, ctx:CMLParser.ValueClusterAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#value.
    def visitValue(self, ctx:CMLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueAttribute.
    def visitValueAttribute(self, ctx:CMLParser.ValueAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#valueStakeholder.
    def visitValueStakeholder(self, ctx:CMLParser.ValueStakeholderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#rawStatement.
    def visitRawStatement(self, ctx:CMLParser.RawStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#idList.
    def visitIdList(self, ctx:CMLParser.IdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CMLParser#qualifiedName.
    def visitQualifiedName(self, ctx:CMLParser.QualifiedNameContext):
        return self.visitChildren(ctx)



del CMLParser