# from .authentication import TokenAuthentication
# from rest_framework.response import Response
# from rest_framework import status, exceptions
#
#
# class TokenAuthMixin:
#     def dispatch(self, request, *args, **kwargs):
#         auth = TokenAuthentication()
#         user, error = auth.authenticate(request)
#
#         if error:
#             response = Response(
#                 {"detail": "Authentication failed", "error": str(error)},
#                 status=status.HTTP_400_BAD_REQUEST,
#                 content_type="application/json"
#             )
#
#             response.accepted_renderer = self.get_renderer(request)
#             response.accepted_media_type = self.content_negotiation_class().select_renderer(request, self.get_renderers())[0].media_type
#             response.renderer_context = self.get_renderer_context()
#             return response
#
#         request.user = user
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_renderer(self, request):
#         renderers = self.get_renderers()
#         renderer = self.content_negotiation_class().select_renderer(request, renderers)[0]
#         return renderer